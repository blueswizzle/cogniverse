# src/api/server.py

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os
import json

from src.lore_loader import load_lore, load_npc_profiles
from src.quests.quest_generator import QuestGenerator
from src.npc.main_npc_dialogue import start_npc_chat  # Optional: can be adapted for API use
from src.agents.multi_agent import MultiAgentPipeline

app = FastAPI(title="Cogniverse API", version="1.0")

# Load lore and NPCs at startup
LORE = load_lore()
NPCS = load_npc_profiles()

# -----------------------
# Request & Response Models
# -----------------------
class NPCChatRequest(BaseModel):
    npc_name: str
    player_input: str

class QuestRequest(BaseModel):
    npc_name: str
    location: Optional[str] = None

# -----------------------
# API Endpoints
# -----------------------
@app.get("/")
def index():
    return {"message": "Welcome to the Cogniverse API!"}

@app.post("/npc/chat")
def npc_chat(req: NPCChatRequest):
    npc_name = req.npc_name
    if npc_name.lower() not in NPCS:
        return {"error": f"NPC '{npc_name}' not found."}

    pipeline = MultiAgentPipeline(NPCS[npc_name.lower()], LORE)
    reply = pipeline.generate_response(req.player_input)

    return {
        "npc_name": npc_name,
        "player_input": req.player_input,
        "npc_reply": reply
    }

@app.post("/quest/generate")
def generate_quest(req: QuestRequest):
    npc_name = req.npc_name
    if npc_name.lower() not in NPCS:
        return {"error": f"NPC '{npc_name}' not found."}

    generator = QuestGenerator(LORE, NPCS)
    quest = generator.generate_quest(npc_name)

    # --- Force output folder to src/quests/generated/game_engine_quests ---
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_dir = os.path.join(BASE_DIR, "src", "quests", "generated", "game_engine_quests")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    quest_file = os.path.join(output_dir, f"{quest['id']}.json")
    with open(quest_file, "w", encoding="utf-8") as f:
        json.dump(quest, f, indent=4, ensure_ascii=False)

    return {"quest": quest}

if __name__ == "__main__":
    uvicorn.run("src.api.server:app", host="127.0.0.1", port=8000, reload=True)
