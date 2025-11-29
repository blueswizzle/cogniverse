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
You are analyzing player input for an NPC in a fantasy RPG.
NPC Name: {npc_name}

Existing Memory:
{existing_memory or "None"}

Player says: "{player_input}"

Task:
- Extract new relevant facts about the player or the world.
- Categorize into SHORT-TERM (session-relevant) or LONG-TERM (persisted info like player name, important traits).
- Output JSON only with keys 'short_term' and 'long_term'.
- Do not include unnecessary info.

JSON format example:
{{
  "short_term": {{}},
  "long_term": {{}}
}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        text = response.choices[0].message.content.strip()
        print(f"{text}")
        mem_data = json.loads(text)
    except Exception:
        mem_data = {"short_term": {}, "long_term": {}}

    return mem_data
