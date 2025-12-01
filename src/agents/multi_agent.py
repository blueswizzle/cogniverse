from src.agents.creator_agent import CreatorAgent
from src.agents.review_agent import LoreReviewerAgent, ToneReviewerAgent
from src.npc_memory.memory_manager import add_short_term, add_long_term, get_short_term, get_long_term
from src.npc_memory.memory_parser import parse_player_input_for_memory

class MultiAgentPipeline:
    def __init__(self, npc_profile, lore):
        self.creator = CreatorAgent(npc_profile, lore)
        self.lore_reviewer = LoreReviewerAgent()
        self.tone_reviewer = ToneReviewerAgent()
        self.lore = lore
        self.npc = npc_profile

    def generate_response(self, player_input):
        # Include current memory in prompt
        short_mem = get_short_term(self.npc['name'])
        long_mem = get_long_term(self.npc['name'])

        memory_context = "NPC Memory:\n"

        if short_mem:
            memory_context += "Short-term facts:\n" + "\n".join(f"- {m}" for m in short_mem) + "\n"

        if long_mem:
            memory_context += "Long-term knowledge:\n" + "\n".join(f"{k}: {v}" for k, v in long_mem.items()) + "\n"

        # --- Use AI to parse input into memory ---
        new_mem = parse_player_input_for_memory(self.npc['name'], player_input, memory_context)

        for fact in new_mem.get("short_term", []):
            add_short_term(self.npc['name'], fact)

        for k, v in new_mem.get("long_term", {}).items():
            add_long_term(self.npc['name'], k, v)


        # Generate NPC reply with memory included
        draft = self.creator.generate(f"{player_input}\n\nNPC Memory Context:\n{memory_context}")

        # Review and refine
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
