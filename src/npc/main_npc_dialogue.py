import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from ..lore_loader import load_lore, load_npc_profiles
from ..agents.multi_agent import MultiAgentPipeline

def main():
    lore = load_lore()
    npcs = load_npc_profiles()
    
    npc_name = "laeris"

    pipeline = MultiAgentPipeline(npcs[npc_name], lore)

    print(f"Chat with {npc_name} — type 'quit' to exit\n")

    while True:
        player = input("You: ")

        if player.lower() in ["quit", "exit"]:
            print("Goodbye, traveler.")
            break

        reply = pipeline.generate_response(player)
        print(f"Laeris: {reply}\n")

if __name__ == "__main__":
    main()
