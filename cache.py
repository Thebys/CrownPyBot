import hashlib
import json
import random
import config
from pathlib import Path


def text_to_hash(text):
    """Generate a 29 character hash from a string.
        - Used for audio cache file names.
        - Changing the hash will break the cache."""
    hash = hashlib.sha256(text.encode()).hexdigest()
    return hash[:29]


def select_random_text():
    """Select a random text line from the database file."""
    # Read the data from the database file
    with open(Path(config.DATABASE_FILE), "r") as f:
        data = json.load(f)

    # Select a random text line
    random_index = random.randint(0, len(data) - 1)
    random_text = data[random_index]["text"]

    return random_text


def create_entry(text, state=None, event=None):
    """Create a new entry in the database file."""
    hash = text_to_hash(text.strip())

    # Read current data from database file
    try:
        with open(Path(config.DATABASE_FILE), "r") as f:
            data = json.load(f)
    except:
        data = []

    # Get next available id
    if len(data) > 0:
        next_id = max([entry["id"] for entry in data]) + 1
    else:
        next_id = 1

    # Create new entry regardless of if source event is available
    if event is None:
        event = {"type": None, "data": None}
        entry = {
            "id": next_id,
            "text": text,
            "hash": hash,
            "state": state,
            "event": event
        }
    else:
        entry = {
            "id": next_id,
            "text": text,
            "hash": hash,
            "state": state,
            "event": {"type": event.type.name, "data": event.data}
        }

    # Append new entry to data
    data.append(entry)

    # Write updated data to database file
    with open(Path(config.DATABASE_FILE), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    return entry


def get_or_create_entry(text, state=None, event=None):
    """Get an entry from the database file or create a new one if it doesn't exist."""
    # Read current data from database file
    try:
        with open(Path(config.DATABASE_FILE), "r") as f:
            data = json.load(f)
    except:
        data = []

    # Check if text is already in database
    for entry in data:
        if entry["text"] == text:
            return entry

    # If text is not in database, create new entry
    return create_entry(text, state, event)
