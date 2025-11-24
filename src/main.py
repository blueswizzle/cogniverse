from lore_loader import load_lore, load_npc_profiles
from npc_agent import NPCAgent

def main():
    lore = load_lore()
    npcs = load_npc_profiles()

    npc = NPCAgent(npcs["eldric"], lore)

    print("Chat with Eldric (type 'quit' to exit)\n")

    while True:
        player = input("You: ")

        if player.lower() in ["quit", "exit"]:
            print("Goodbye, traveler.")
            break
        
        print("\n....")

        reply = npc.respond(player)
        print(f"Eldric: {reply}\n")

if __name__ == "__main__":
    main()
