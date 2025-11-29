# src/main.py

from src.npc.main_npc_dialogue import start_npc_chat
from src.lore_loader import load_npc_profiles, load_lore
from src.quests.main_quest import generate_and_save_quest
import os
import json

# Utility to save quest JSON
def save_quest_to_json(quest: dict, output_dir=None):
    """
    Save the quest dictionary as a JSON file.
    """
    if output_dir is None:
        # Fixed folder for game engine quests
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "game_engine_quests")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    quest_file = os.path.join(output_dir, f"{quest['id']}.json")
    with open(quest_file, "w", encoding="utf-8") as f:
        json.dump(quest, f, indent=4, ensure_ascii=False)

    print(f"Quest saved to {quest_file}")
    return quest_file

def main():
    print("=== Welcome to Cogniverse ===")
    print("1. Talk to an NPC")
    print("2. Generate a Quest")
    choice = input("Enter choice (1 or 2): ").strip()

    # Load lore & NPCs
    lore = load_lore()
    npcs = load_npc_profiles()
    npc_names = list(npcs.keys())

    if choice == "1":
        print("\nAvailable NPCs:")
        for idx, name in enumerate(npc_names, 1):
            print(f"{idx}. {name.title()}")
        selection = input("Choose an NPC (number or name): ").strip()
        if selection.isdigit() and 1 <= int(selection) <= len(npc_names):
            npc_name = npc_names[int(selection)-1].title()
        elif selection.lower() in [n.lower() for n in npc_names]:
            npc_name = next(n for n in npc_names if n.lower() == selection.lower()).title()
        else:
            print("Invalid selection, defaulting to Laeris.")
            npc_name = "Laeris"

        start_npc_chat(npc_name=npc_name)

    elif choice == "2":
        print("\nAvailable NPCs for quests:")
        for idx, name in enumerate(npc_names, 1):
            print(f"{idx}. {name.title()}")
        selection = input("Choose an NPC to assign the quest: ").strip()
        if selection.isdigit() and 1 <= int(selection) <= len(npc_names):
            npc_name = npc_names[int(selection)-1].title()
        elif selection.lower() in [n.lower() for n in npc_names]:
            npc_name = next(n for n in npc_names if n.lower() == selection.lower()).title()
        else:
            print("Invalid selection, defaulting to Laeris.")
            npc_name = "Laeris"

        # Generate and save quest
        generate_and_save_quest(npc_name, lore, npcs)

    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
