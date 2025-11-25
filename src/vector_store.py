import chromadb
from chromadb.config import Settings
from openai import OpenAI
from config import OPENAI_API_KEY
from tqdm import tqdm
import os
import json

# OpenAI client (same style as prior files)
oai = OpenAI(api_key=OPENAI_API_KEY)

# Use local Chroma (persisted to ./chroma_db)
CHROMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

COLLECTION_NAME = "cogniverse_lore"

def create_or_get_collection():
    return chroma_client.get_or_create_collection(name=COLLECTION_NAME)

def embed_texts(texts):
    """
    Create embeddings using OpenAI embedding model. Expects list[str] -> list[vector]
    """
    # batch embeddings via OpenAI
    resp = oai.embeddings.create(model="text-embedding-3-small", input=texts)
    # resp.data is list of dicts with 'embedding'
    return [d.embedding for d in resp.data]

def clean_metadata(data: dict):
    """Remove None values and cast everything to string-safe types"""
    return {k: str(v) for k, v in data.items() if v is not None}

def index_lore(lore: list, npcs: list):
    print("Indexing lore & NPC profiles to Chroma...")
    collection = create_or_get_collection()

    for i, item in enumerate(lore):
    # If lore is a string, wrap it into dict format
        if isinstance(item, str):
            lore_text = item
            title = f"Lore Entry {i}"
            source = "unknown"
        else:
            lore_text = item.get("text", "")
            title = item.get("title", f"Lore Entry {i}")
            source = item.get("source", "unknown")

    metadata = clean_metadata({
        "type": "lore",
        "title": title,
        "source": source
    })

    collection.add(
        ids=[f"lore_{i}"],
        documents=[lore_text],
        metadatas=[metadata],
    )


    for i, npc in enumerate(npcs):
    # Support both string and dict formats
        if isinstance(npc, str):
            name = f"NPC_{i}"
            role = "unknown"
            description = npc
        else:
            name = npc.get("name", f"NPC_{i}")
            role = npc.get("role", "unknown")
            description = npc.get("description", "")

    metadata = clean_metadata({
        "type": "npc",
        "name": name,
        "role": role
    })

    profile_text = f"{name} is a {role}. {description}"

    collection.add(
        ids=[f"npc_{i}"],
        documents=[profile_text],
        metadatas=[metadata],
    )


    print("Indexing complete.")


def retrieve_context(query: str, k: int = 4):
    collection = create_or_get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    hits = []
    for i in range(len(results["documents"][0])):
        hits.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return hits

