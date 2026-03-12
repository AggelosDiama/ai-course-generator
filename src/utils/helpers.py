import os

def load_prompt(filename):
    """Loads a prompt string from the prompts directory."""
    base_dir = os.path.dirname(os.path.dirname(__file__)) # Go up to src
    path = os.path.join(base_dir, "prompts", filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file {filename} not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()