import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from lore_loader import load_lore, load_npc_profiles
from agents.multi_agent import MultiAgentPipeline

def main():
    lore = load_lore()
    npcs = load_npc_profiles()

    pipeline = MultiAgentPipeline(npcs["laeris"], lore)

    print("Chat with Laeris — type 'quit' to exit\n")

    while True:
        player = input("You: ")

        if player.lower() in ["quit", "exit"]:
            print("Goodbye, traveler.")
            break

        reply = pipeline.generate_response(player)
        print(f"Laeris: {reply}\n")

if __name__ == "__main__":
    main()
