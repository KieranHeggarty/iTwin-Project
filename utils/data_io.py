import json

def load_json(filepath):
    """Load and return data from a JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)

def save_json(data, filepath):
    """Save data to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


