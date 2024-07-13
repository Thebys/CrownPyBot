import hashlib
import sqlite3
import random
import os
import config
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)


def text_to_hash(text):
    """Generate a 29 character hash from a string.
    - Used for audio cache file names.
    - Changing the hash will break the cache."""
    try:
        hash = hashlib.sha256(text.encode()).hexdigest()
        return hash[:29]
    except:
        return None


def select_random_text():
    """Select a random text line from the database file."""
    # Read the data from the database file, choose a random text line
    try:
        db = sqlite3.connect(config.DATABASE_FILE)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM texts ORDER BY RANDOM() LIMIT 1")
        data = cursor.fetchone()
        db.close()
    except:
        data = []
        return None

    # Select a random text line
    random_index = random.randint(0, len(data) - 1)
    random_text = data[random_index]["text"]

    return random_text


def create_entry(text, state=None, event=None):
    """Create a new entry in the database file."""
    if text is None:
        return None

    hash = text_to_hash(text.strip())

    # Create a new text line entry in the database with autoincrement id, hash, text, state, event and audio file path
    try:
        db = sqlite3.connect(config.DATABASE_FILE)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO texts (hash, text, state, event, audio_file_path) VALUES (?, ?, ?, ?, ?)",
            (hash, text, str(state), str(event), f"{config.AUDIO_CACHE_FOLDER}{os.path.sep}{hash}.wav"),
        )
        db.commit()
        db.close()
        logger.info(f"DB - Entry created: {text}")
    except Exception as e:
        logger.error(f"DB - Error creating entry: {e}")
        return None

    entry = {
        "text": text,
        "hash": hash,
        "state": state,
        "event": {
            "type": event.name if event else None,
            "data": event.value if event else None,
        },
    }
    return entry


def get_or_create_entry(text, state=None, event=None):
    """Get an entry from the database file or create a new one if it doesn't exist."""
    TextEntry = namedtuple('TextEntry', ['hash', 'text', 'state', 'event', 'audio_file_path'])
    
    try:
        with sqlite3.connect(config.DATABASE_FILE) as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("SELECT * FROM texts WHERE text = ?", (text,))
            result = cursor.fetchone()
            
            if result:
                entry = TextEntry(**result)
                return {
                    "text": entry.text,
                    "hash": entry.hash,
                    "state": entry.state,
                    "event": {
                        "type": entry.event,
                        "data": None,  # Adjust this if you store event data separately
                    },
                }
    except Exception as e:
        logger.error(f"DB - Error getting entry: {e}")
    
    # If text is not in database or there was an error, create new entry
    return create_entry(text, state, event)
