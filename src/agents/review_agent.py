from openai import OpenAI
from ..config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

class LoreReviewerAgent:
    def review(self, draft, lore):
        prompt = f"""
Check if the following NPC reply violates or contradicts this world lore:

WORLD LORE:
{lore}

NPC REPLY:
{draft}

If there is a contradiction, explain it briefly.
If not, reply "OK".
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class ToneReviewerAgent:
    def review(self, draft, npc_profile):
        prompt = f"""
Check if the tone of the reply matches this NPC:

Personality: {npc_profile['personality']}
Speech Style: {npc_profile['speech_style']}

NPC REPLY:
{draft}

If tone is wrong, explain why. If fine, reply "OK".
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
