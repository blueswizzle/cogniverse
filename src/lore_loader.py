import json

WORLD_LORE_PATH = "data/world_lore.json"
NPC_PROFILES_PATH = "data/npc_profiles.json"

def load_lore(path=WORLD_LORE_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_npc_profiles(path=NPC_PROFILES_PATH):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
