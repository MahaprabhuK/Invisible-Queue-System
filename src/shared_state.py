import json
import os

STATE_FILE = "data/counter_state.json"

def get_state(counter_id):
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                state = json.load(f)
                return state.get(str(counter_id), {})
            except:
                pass
    return {}

def update_state(counter_id, data):
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                state = json.load(f)
            except:
                pass
    
    if str(counter_id) not in state:
        state[str(counter_id)] = {}
        
    state[str(counter_id)].update(data)
    
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
