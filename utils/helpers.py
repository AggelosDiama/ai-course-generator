import os

def load_prompt(filename):
    """Loads a prompt string from the prompts directory."""
    path = os.path.join("prompts", filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file {filename} not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()