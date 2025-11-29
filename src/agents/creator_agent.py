from openai import OpenAI
from ..config import OPENAI_API_KEY
from ..vector_store import retrieve_context
import json

client = OpenAI(api_key=OPENAI_API_KEY)

class CreatorAgent:
    def __init__(self, npc_profile, lore):
        self.npc = npc_profile
        self.lore = lore

    def generate(self, player_input):
        # Retrieve top-k relevant lore snippets for grounding
        retrieval_query = f"Player asks: {player_input}\nNPC: {self.npc.get('name')}\nGoal: find relevant lore facts."
        hits = retrieve_context(retrieval_query, k=4)

        # Build a grounded context string
        context_parts = []
        for i, h in enumerate(hits):
            meta = h.get("meta", {})
            context_parts.append(f"[source {i+1} | {meta.get('type')} | {meta.get('name', meta.get('npc_key', ''))}]\n{h.get('text')}\n")

        grounded_context = "\n---\n".join(context_parts)

        prompt = f"""
You are the NPC {self.npc['name']} in the world of {self.lore.get('world_name', 'the world')}.
Personality: {self.npc.get('personality')}
Backstory: {self.npc.get('backstory')}
Speech Style: {self.npc.get('speech_style')}

Grounded relevant facts (from the game's lore database):
{grounded_context}

Player said: "{player_input}"

Instructions:
- Keep your response concise (1–3 sentences).  
- Speak in-character and stay consistent with your personality and lore.  
- Adjust tone based on player intent:
  * Friendly → polite, helpful
  * Neutral → neutral
  * Threat / aggression → defensive, cautious, or evasive
- If the topic is unknown, respond cautiously without inventing canonical facts.

When the player is threatening:
- Do NOT respond poetically
- Do NOT try to calm them peacefully
- Respond with warnings, boundaries, or consequences
- You may imply guards, magic defenses, or reputation damage
- Never describe graphic violence
- Never encourage real-world harm

Respond appropiately:
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a game NPC. Use only the provided canonical facts to stay consistent."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
