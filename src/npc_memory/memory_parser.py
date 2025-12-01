import json
from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_player_input_for_memory(npc_name, player_input, existing_memory=""):
    """
    Use AI to extract facts from player input for memory storage.
    Returns a dict with 'short_term' and 'long_term' keys.
    """
    prompt = f"""
You are an AI assisting an NPC in a fantasy RPG.

Your job is to extract facts from the PLAYER'S input and categorize them:

SHORT-TERM MEMORY (session only)
- transient facts
- emotional reactions
- temporary goals
- current location
- recent actions

LONG-TERM MEMORY (persistent)
- player name
- player race / class / role
- permanent traits
- relationships
- backstory elements
- NPC promises
- Oaths or commitments
- Long-term goals

OUTPUT FORMAT:
{{
  "short_term": [ "fact1", "fact2" ],
  "long_term":  {{ "key": "value" }}
}}

RULES:
- Never rewrite or remove existing memory.
- Only add new facts.
- Use simple, structured facts.
- If player says "My name is X", save: {{ "name": "X" }} in long_term.
- If player describes themselves (e.g., "I'm a spellsword"), save in long_term.

Existing memory:
{existing_memory or "None"}

Player says: "{player_input}"
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        text = response.choices[0].message.content.strip()
        mem_data = json.loads(text)
    except Exception:
        mem_data = {"short_term": {}, "long_term": {}}

    return mem_data
