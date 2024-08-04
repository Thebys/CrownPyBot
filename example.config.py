# OpenAI API configuration
OPENAI_API_KEY = "your_openai__api_key_here"
OPENAI_API_CHAT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
OPENAI_CHAT_MODEL = "gpt-4o"
OPENAI_CHAT_MODEL_MAX_TOKENS = 127800
# Google Text-to-Speech API configuration
GOOGLE_TTS_API_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize"
GOOGLE_KEYFILE_PATH = "keyfile.json"

# Telegram Bot API configuration
TG_BOT_TOKEN =  "your_telegram_bot_token_here"

# Database configuration
DATABASE_FILE = "database/database.sqlite"

# Audio cache folder configuration
AUDIO_CACHE_FOLDER = "audio"

# Behavior settings - currently true enables AI/TTS generation loop
LEARNING = True
LANGUAGE = "English"
# LANGUAGE = "Czech"

# Development settings - Enables debug logging and adds random events to the event queue
DEVELOPMENT = False
