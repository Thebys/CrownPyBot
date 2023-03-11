import config
import logging
import cache
import os
from pathlib import Path
from google.cloud import texttospeech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_KEYFILE_PATH


def download_audio(Prompt, LangCode="de-DE", VoiceName="de-DE-Wavenet-E", Pitch=5.2, SprakingRate=1.0):
    """Download audio file from Google TTS API and cache it."""
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=Prompt)
    voice = texttospeech.VoiceSelectionParams(
        language_code=LangCode, name=VoiceName
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, pitch=Pitch, speaking_rate=SprakingRate
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    file_name = cache.text_to_hash(Prompt) + ".wav"
    file_path = Path(config.AUDIO_CACHE_FOLDER, file_name).resolve()

    with open(file_path, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        logging.debug(f"Saved audio file for text:\n {Prompt} as {file_path}.")
