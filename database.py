import json
import os

def load_json(file_path):
    """Safely load a JSON file and return its data as a Python dictionary."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Return empty dict if file is corrupted or empty
            return {}
    return {}

def save_json(file_path, data):
    """Save a Python dictionary into a JSON file (creates file if not exists)."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
