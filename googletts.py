import config
import logging
import AudioCache
import os
from pathlib import Path
from google.cloud import texttospeech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_KEYFILE_PATH

def energy_enum_to_speaking_rate(Energy):
    energy_based_speaking_rate = 0.95
    if Energy == Energy.EXHAUSTED:
        energy_based_speaking_rate = 0.75
    elif Energy == Energy.TIRED:
        energy_based_speaking_rate = 0.85
    elif Energy == Energy.NORMAL:
        energy_based_speaking_rate = 0.95
    elif Energy == Energy.ENERGIZED:
        energy_based_speaking_rate = 1.10
    elif Energy == Energy.HYPER:
        energy_based_speaking_rate = 1.20
    return energy_based_speaking_rate


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

    file_name = AudioCache.text_to_hash(Prompt) + ".wav"
    file_path = Path(config.AUDIO_CACHE_FOLDER, file_name).resolve()

    try:
        with open(file_path, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
        logging.debug(f"FS - Saved audio file: {file_path}.")
    except:
        logging.error(f"FS - Error saving audio file: {file_path}.")

def download_audio_czech(Prompt, LangCode="cs-CZ", VoiceName="cs-CZ-Wavenet-A", Pitch=-18, SpeakingRate=0.85):
    """Download audio file from Google TTS API and cache it."""
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=Prompt)
    voice = texttospeech.VoiceSelectionParams(
        language_code=LangCode, name=VoiceName
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, pitch=Pitch, speaking_rate=SpeakingRate
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    file_name = AudioCache.text_to_hash(Prompt) + ".wav"
    file_path = Path(config.AUDIO_CACHE_FOLDER, file_name).resolve()

    with open(file_path, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        logging.debug(f"FS - Saved audio file: {file_path}.")