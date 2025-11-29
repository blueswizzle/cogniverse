import json
import uuid
from typing import Dict
from openai import OpenAI
from src.config import OPENAI_API_KEY
import re

client = OpenAI(api_key=OPENAI_API_KEY)

class QuestGenerator:
    """
    Generates dynamic quests using GenAI based on NPCs and world context.
    """

    def __init__(self, lore: Dict, npcs: Dict):
        self.lore = lore
        self.npcs = npcs

    def generate_quest(self, npc_name: str) -> Dict:
        """
        Generates a quest for a given NPC via AI.
        Returns a JSON-compatible dict containing quest info.
        """
        npc = self.npcs.get(npc_name.lower())
        if not npc:
            npc = self.npcs.get("laeris")  # default NPC

        prompt = f"""
You are a game quest designer. Generate a quest for the following NPC
based on their personality, role, backstory, and the world lore.

NPC:
Name: {npc['name']}
Personality: {npc['personality']}
Role: {npc['role']}
Speech Style: {npc['speech_style']}

World Lore:
{self.lore.get('world_summary', 'No summary available')}

Output the quest as a JSON object with these keys:
- id: unique quest identifier
- title: quest title
- giver: NPC name
- objectives: list of objectives with type, target/item, location, amount
- rewards: dict with xp, gold, items
- dialogue: what the NPC says to give the quest

Only output valid JSON.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        quest_text = response.choices[0].message.content
        
        # Strip code fences if present
        quest_text = re.sub(r"^```(?:json)?|```$", "", quest_text, flags=re.MULTILINE).strip()
        
        # Log the raw GPT response for debugging
        # print("=== GPT Raw Response ===")
        # print(quest_text)
        # print("========================")

        try:
            quest = json.loads(quest_text)
        except json.JSONDecodeError:
            # fallback in case AI outputs invalid JSON
            quest = {
                "id": str(uuid.uuid4()),
                "title": f"{npc['name']}'s Quest",
                "giver": npc['name'],
                "objectives": [],
                "rewards": {},
                "dialogue": f"{npc['name']}: I need your help with something urgent."
            }

        return quest
