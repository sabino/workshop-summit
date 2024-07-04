import os
import yaml

STATE_FILE = 'data/state/state.yml'

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as file:
            return yaml.safe_load(file)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as file:
        yaml.safe_dump(state, file)
