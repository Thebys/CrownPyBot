"""
Database.py

Handle database operations, create tables, insert, update, delete, checks, etc.
"""

import hashlib
import sqlite3
import random
import os
import config
import logging

class Database:
    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def check_or_init_db(self):
        """
        Check if database exists, if not create it
        """
        if not os.path.exists(config.DATABASE_FILE):
            self.logger.warning(f"Database {config.DATABASE_FILE} does not exist!")
            self.create_db()

    def check_or_init_tables(self):
        """
        Check if tables exist, if not create them
        """    
        with sqlite3.connect(config.DATABASE_FILE) as db:
            cursor = db.cursor()
            if not cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='texts';").fetchone():
                self.logger.warning("Audio Cache Table does not exist! Creating.")
                # Audio Cache Table -~ SELECT id, hash, text, state, audio_file_path FROM texts
                cursor.execute("""CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT,
                text TEXT,
                state TEXT,
                audio_file_path TEXT
            );""")




    def create_db(self):
        """
        (Only) Create empty database
        """
        with sqlite3.connect(config.DATABASE_FILE) as db:
            cursor = db.cursor()

            # Create texts table
            cursor.execute("""VACUUM;""")

            db.commit()
            self.logger.info(f"Database created successfully as {config.DATABASE_FILE}")
