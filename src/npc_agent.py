from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

class NPCAgent:
    def __init__(self, npc_profile, lore):
        self.profile = npc_profile
        self.lore = lore

    def respond(self, player_input):
        prompt = f"""
You are the NPC {self.profile['name']}.

Personality: {self.profile['personality']}
Backstory: {self.profile['backstory']}
Speech Style: {self.profile['speech_style']}

Relevant World Lore:
{self.lore}

The player asks: "{player_input}"

Respond in character. Stay consistent with lore, tone, and personality.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an NPC in a fantasy RPG."},
                {"role": "user", "content": prompt},
            ]
        )

        return response.choices[0].message["content"]
