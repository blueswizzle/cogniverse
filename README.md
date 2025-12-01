# Cogniverse

Cogniverse is a virtual startup redefining how video game worlds evolve by embedding Generative Intelligence into the heart of RPGs and open-world games. Modern games, though vast and beautifully handcrafted, remain static once players complete their scripted content, forcing studios to invest heavily in post-launch updates to sustain engagement.  

Cogniverse addresses this limitation by introducing a generative system that dynamically creates lore-consistent quests, dialogue, characters, and world events, expanding each game’s world intelligently and endlessly.  

At its core, Cogniverse uses multi-agent generative AI that learns from the game’s existing lore and artistic design, ensuring all new content aligns with the established tone and rules of the game world. This solution directly enhances the design, development, and maintenance stages of the Software Development Lifecycle by automating content creation, augmenting creative design, and enabling worlds that continuously grow long after release.

---

## Note

This is an **early prototype (MVP)**. It demonstrates core AI-driven concepts like NPC conversations, memory, and quest generation, but it is **nowhere near a finished product**. Features are limited, integrations with actual game engines are minimal, and stability/performance has not been fully tested.  

---

## Implemented Features

### 1. AI NPC Conversations
- NPCs respond **in-character** based on personality, backstory, and speech style.
- Multi-agent pipeline:
  - **Creator Agent** generates initial NPC responses.
  - **Lore Reviewer** checks consistency with world lore.
  - **Tone Reviewer** ensures NPC personality is preserved.
- Players can interact with NPCs via console chat.
- **Commands**:
  - `!memory` — view short-term and long-term memory.
  - `!clear` — reset memory (short or long-term).

### 2. NPC Memory
- **Short-term memory:** Stores per-session information (e.g., facts mentioned during the conversation).
- **Long-term memory:** Persists NPC knowledge across sessions (`long_term_memory.json`).
- NPCs can automatically remember important facts without explicit keywords using AI parsing.

### 3. Dynamic Quest Generation
- AI generates quests for NPCs based on:
  - NPC personality, role, and backstory
  - World lore
- Quest output is **JSON-compatible** and includes:
  - Unique `id` (UUID)
  - Title
  - Quest giver
  - Objectives
  - Rewards
  - Dialogue
- Each quest is saved as a separate JSON file for use by a game engine.

### 4. FastAPI REST Server
- Includes a lightweight **FastAPI** server that exposes AI features to any game engine (Unity, Unreal, Godot, custom engines, etc.).
- Available endpoints include:

#### Endpoints

1. **`POST /npc/chat`**  
   - Send a message to an NPC and receive their AI-generated response.  
   - **Request Body:**
     ```json
     {
       "npc_name": "laeris",
       "player_input": "Hello there, how are you?"
     }
     ```
   - **Response:**
     ```json
     {
       "npc_name": "laeris",
       "player_input": "Hello there, how are you?",
       "npc_reply": "I am well, traveler. What brings you to these woods?"
     }
     ```

2. **`POST /quest/generate`**  
   - Generate a dynamic quest for a specific NPC based on their personality, role, and world lore.  
   - **Request Body:**
     ```json
     {
       "npc_name": "laeris"
     }
     ```
   - **Response:**
     ```json
     {
      "title": "Laeris Willowstride's Quest",
      "giver": "Laeris Willowstride",
      "objectives": [],
      "rewards": {},
      "dialogue": "Laeris Willowstride: I need your help with something urgent.",
      "id": "83e8eadd-6238-419f-9bbd-a2c1149edf6a"
      }
     ```
  

## Getting Started

Follow these steps to set up and run the Cogniverse prototype locally.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/cogniverse.git
cd cogniverse
```

### 2. Create the python virtual environment
```bash
python3 -m venv .venv
```
### 3. Activate virtual environment
- Windows:
  ```bash
  .venv\Scripts\Activate.ps1
  ```
- MacOS/Linux
  ```bash
  source .venv/bin/activate
  ```
### 4. Install required packages
```bash
pip install -r requirements.txt
```
### 5. Create a *.env* file at the root of the project. Next go to OpenAI's website and generate an Open AI API Key. Once you have it, inside the *.env* file add your key
```bash
OPENAI_API_KEY=your_openai_api_key_here
```
