import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from src.lore_loader import load_lore, load_npc_profiles
from src.agents.multi_agent import MultiAgentPipeline

def start_npc_chat(npc_name="Laeris"):
    # Load lore & NPC profiles
    lore = load_lore()
    npcs = load_npc_profiles()

    if npc_name.lower() not in npcs:
        print(f"NPC '{npc_name}' not found. Defaulting to Laeris.")
        npc_name = "Laeris"

    pipeline = MultiAgentPipeline(npcs[npc_name.lower()], lore)

    print(f"\nChat with {npc_name} — type 'quit' to exit\n")

    while True:
        player_input = input("You: ")
        if player_input.lower() in ["quit", "exit"]:
            print("Goodbye, traveler.")
            break

        reply = pipeline.generate_response(player_input)
        print(f"{npc_name}: {reply}\n")


# Optional: allow direct run for testing
if __name__ == "__main__":
    start_npc_chat()
