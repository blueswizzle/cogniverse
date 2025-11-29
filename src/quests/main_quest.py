# src/quests/main_quest.py

import json
from src.quests.quest_generator import QuestGenerator
import os

def save_quest_to_json(quest: dict, output_dir=None):
    """
    Save the quest dictionary as a JSON file.
    """
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "game_engine_quests")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    quest_file = os.path.join(output_dir, f"{quest['id']}.json")
    with open(quest_file, "w", encoding="utf-8") as f:
        json.dump(quest, f, indent=4, ensure_ascii=False)

    print(f"Quest saved to {os.path.abspath(quest_file)}")
    return quest_file


def generate_and_save_quest(npc_name: str, lore: dict, npcs: dict):
    """
    Generate a quest for the given NPC using AI, save it to JSON, and print it.
    """
    generator = QuestGenerator(lore, npcs)
    quest = generator.generate_quest(npc_name)

    # Save quest JSON to fixed folder
    save_quest_to_json(quest)

    print("\n=== Generated Quest ===\n")
    print(json.dumps(quest, indent=4, ensure_ascii=False))
