import config
import logging
import cache

from google.cloud import texttospeech


def download_audio(Prompt, LangCode="de-DE", VoiceName="de-DE-Wavenet-E", Pitch=5.2, SprakingRate=1.0):

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

    filename = config.AUDIO_CACHE_FOLDER+"/"+cache.text_to_hash(Prompt)+".wav"
    with open(filename, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        logging.debug("Saved audio file for text: """+Prompt + " as "+filename)
