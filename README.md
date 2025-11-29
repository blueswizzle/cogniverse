# Cogniverse — AI-Driven NPCs & Dynamic Quests

**Cogniverse** is a prototype RPG engine that demonstrates AI-driven NPC interactions, dynamic quest generation, and memory management. 
This project leverages OpenAI's GPT models to create immersive, context-aware NPCs that remember past interactions and generate quests dynamically based on world lore.

---

## Features

### 1. AI NPC Conversations
- NPCs respond in-character based on personality, backstory, and speech style.
- Multi-agent pipeline:
  - **Creator Agent** generates initial NPC responses.
  - **Lore Reviewer** checks consistency with world lore.
  - **Tone Reviewer** ensures NPC personality is preserved.
- Players can interact with NPCs via console chat.
- Commands:
  - `!memory` — view short-term and long-term memory.
  - `!clear` — reset memory (short or long-term).

### 2. NPC Memory
- **Short-term memory:** Stores per-session information (e.g., facts mentioned during the conversation).
- **Long-term memory:** Persists NPC knowledge across sessions (`long_term_memory.json`).
- NPCs can automatically remember important facts without explicit keywords using AI parsing.

### 3. Dynamic Quest Generation
- AI generates quests for NPCs based on:
  - NPC personality, role, and backstory.
  - World lore.
- Quest output is JSON-compatible and includes:
  - Unique `id` (UUID)
  - Title
  - Quest giver
  - Objectives
  - Rewards
  - Dialogue
- Each quest is saved as a separate JSON file for use by a game engine.
