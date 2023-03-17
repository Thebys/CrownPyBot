# OpenAI GPT-3 API configuration
OPENAI_API_KEY = "your_openai__api_key_here"
OPENAI_API_COMPLETIONS_ENDPOINT = "https://api.openai.com/v1/completions"
OPENAI_API_CHAT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
OPENAI_COMPLETIONS_MODEL = "text-davinci-003"
OPENAI_CHAT_MODEL = "gpt-3.5-turbo"
# Google Text-to-Speech API configuration
GOOGLE_TTS_API_KEY = "your_google_tts_api_key_here"
GOOGLE_TTS_API_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize"
GOOGLE_KEYFILE_PATH = "keyfile.json"
# Database configuration
DATABASE_FILE = "database/cache.json"

# Audio cache folder configuration
AUDIO_CACHE_FOLDER = "audio"

# Behavior settings - currently true enables AI/TTS generation loop
LEARNING = True
LANGUAGE = "English"
# LANGUAGE = "Czech"

# Development settings - Enables debug logging and adds random events to the event queue
DEVELOPMENT = False
