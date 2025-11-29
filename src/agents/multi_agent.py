from src.agents.creator_agent import CreatorAgent
from src.agents.review_agent import LoreReviewerAgent, ToneReviewerAgent

class MultiAgentPipeline:
    def __init__(self, npc_profile, lore):
        self.creator = CreatorAgent(npc_profile, lore)
        self.lore_reviewer = LoreReviewerAgent()
        self.tone_reviewer = ToneReviewerAgent()
        self.lore = lore
        self.npc = npc_profile

    def generate_response(self, player_input):
        draft = self.creator.generate(player_input)

        lore_check = self.lore_reviewer.review(draft, self.lore)
        tone_check = self.tone_reviewer.review(draft, self.npc)

        if lore_check != "OK" or tone_check != "OK":
            refinement_prompt = f"""
Fix the following NPC reply.

ISSUES:
Lore Review: {lore_check}
Tone Review: {tone_check}

Original Reply:
{draft}
"""
            draft = self.creator.generate(refinement_prompt)

        return draft
