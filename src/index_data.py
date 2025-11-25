from lore_loader import load_lore, load_npc_profiles
from vector_store import index_lore

def main():
    lore = load_lore()
    npcs = load_npc_profiles()
    print("Indexing lore & NPC profiles to Chroma...")
    index_lore(lore, npcs)
    print("Indexing complete.")

if __name__ == "__main__":
    main()
