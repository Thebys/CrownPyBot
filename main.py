import config
import pygame
import logging
import cache
import openai
import googletts
import os
import time
# def get_audio_file(text_input):
# Check if audio file is already in the cache
# If it is, return the file name
# If it is not, generate a new audio file and save it to the cache

# Code to make API request to Google Text-to-Speech API
# Code to save audio file to cache folder
# Code to update database with new text input and corresponding audio file name


def play_audio_file(file_name):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load(config.AUDIO_CACHE_FOLDER +"/"+ file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    logging.debug("Playing sound finished.")

def main():
    logging.basicConfig(filename="CrownPiBot.log", level=logging.DEBUG)
    # Code to read text inputs from database
    # Code to get audio file for each text input
    # Code to play audio file for each text input
    newline = openai.generate_text(
        "A vintage crown gambling machine comes to life after collecting dust for 30 years and says this punchline: ")
    file_name = cache.text_to_hash(newline)+".wav"
    file_path = config.AUDIO_CACHE_FOLDER + file_name
    cache.get_or_create_entry(config.DATABASE_FILE, newline)
    if os.path.exists(file_path):
        logging.debug(f"Cache hit! The file {file_path} exists.")
    else:
        logging.warn(f"Cache miss! The file {file_path} doesn't exists.")
        googletts.download_audio(newline)

    play_audio_file(file_name)


if __name__ == "__main__":
    main()
