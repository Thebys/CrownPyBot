import hashlib
import json

def text_to_hash(text):
    hash = hashlib.sha256(text.encode()).hexdigest()
    return hash[:29]

def create_entry(database_file, text):
    # Generate hash of text
    hash = text_to_hash(text.strip())

    # Read current data from database file
    try:
        with open(database_file, "r") as f:
            data = json.load(f)
    except:
        data = []

    # Get next available id
    if len(data) > 0:
        next_id = max([entry["id"] for entry in data]) + 1
    else:
        next_id = 1

    # Create new entry
    entry = {
        "id": next_id,
        "text": text,
        "hash": hash
    }

    # Append new entry to data
    data.append(entry)

    # Write updated data to database file
    with open(database_file, "w") as f:
        json.dump(data, f)

    return entry

def get_or_create_entry(database_file, text):
    # Read current data from database file
    try:
        with open(database_file, "r") as f:
            data = json.load(f)
    except:
        data = []

    # Check if text is already in database
    for entry in data:
        if entry["text"] == text:
            return entry

    # If text is not in database, create new entry
    return create_entry(database_file, text)