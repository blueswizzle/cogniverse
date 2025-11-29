import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from src.lore_loader import load_lore, load_npc_profiles
from src.agents.multi_agent import MultiAgentPipeline
from src.npc_memory.memory_manager import (
    get_short_term,
    get_long_term,
    clear_short_term,
    clear_long_term
)

def start_npc_chat(npc_name="Laeris"):
    # Load lore & NPC profiles
    lore = load_lore()
    npcs = load_npc_profiles()

    if npc_name.lower() not in npcs:
        print(f"NPC '{npc_name}' not found. Defaulting to Laeris.")
        npc_name = "Laeris"

    pipeline = MultiAgentPipeline(npcs[npc_name.lower()], lore)

    print(f"\nChat with {npc_name} — type 'quit' to exit")
    print("Special commands: !memory, !short, !long, !clear")

    while True:
        player_input = input("You: ").strip()

        if player_input.lower() in ["quit", "exit"]:
            print("Goodbye, traveler.")
            break

       # Handle special commands
        if player_input.startswith("!"):
            cmd = player_input[1:].lower()
            if cmd == "memory":
                print(f"\n--- {npc_name}'s Memory ---")
                print("Short-term memory:", get_short_term(npc_name))
                print("Long-term memory:", get_long_term(npc_name))
            elif cmd == "short":
                print(f"\n--- {npc_name}'s Short-Term Memory ---")
                print(get_short_term(npc_name))
            elif cmd == "long":
                print(f"\n--- {npc_name}'s Long-Term Memory ---")
                print(get_long_term(npc_name))
            elif cmd == "clear":
                clear_short_term(npc_name)
                clear_long_term(npc_name)
                print(f"{npc_name}'s memory cleared.")
            continue

        # Normal conversation
        reply = pipeline.generate_response(player_input)
        print(f"{npc_name}: {reply}\n")


# Optional: allow direct run for testing
if __name__ == "__main__":
    start_npc_chat()
