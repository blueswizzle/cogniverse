import json
import os

SHORT_TERM_MEMORY = {}  # per-session
LONG_TERM_FILE = os.path.join(os.path.dirname(__file__), "long_term_memory.json")

# Load long-term memory if exists
if os.path.exists(LONG_TERM_FILE):
    with open(LONG_TERM_FILE, "r", encoding="utf-8") as f:
        LONG_TERM_MEMORY = json.load(f)
else:
    LONG_TERM_MEMORY = {}

# --- Short-term memory ---
def add_short_term(npc_name, value):
    npc_name = npc_name.lower()
    if npc_name not in SHORT_TERM_MEMORY:
        SHORT_TERM_MEMORY[npc_name] = []
    SHORT_TERM_MEMORY[npc_name].append(value)

def get_short_term(npc_name):
    return SHORT_TERM_MEMORY.get(npc_name.lower(), [])

def clear_short_term(npc_name):
    SHORT_TERM_MEMORY[npc_name.lower()] = {}
    
def clear_long_term(npc_name):
    LONG_TERM_MEMORY[npc_name.lower()] = {}

# --- Long-term memory ---
def add_long_term(npc_name, key, value):
    npc_name = npc_name.lower()
    if npc_name not in LONG_TERM_MEMORY:
        LONG_TERM_MEMORY[npc_name] = {}

    # Only write if new or updated
    LONG_TERM_MEMORY[npc_name][key] = value
    save_long_term()

def get_long_term(npc_name):
    return LONG_TERM_MEMORY.get(npc_name.lower(), {})

def save_long_term():
    with open(LONG_TERM_FILE, "w", encoding="utf-8") as f:
        json.dump(LONG_TERM_MEMORY, f, indent=4, ensure_ascii=False)
