from enum import Enum
from pathlib import Path
import random
import logging
import config
import pygame
import cache
import openai
import googletts
import time
from events import EventQueue, EventTypes, Event

# This set of classes is the brain of the machine. It is responsible for the machine's state and behavior.
# The MachineBrain is a singleton class, so there can only be one instance of it at a time.


class EnergyLevel(Enum):
    """Energy level palette of the machine."""
    EXHAUSTED = 1
    TIRED = 2
    NORMAL = 3
    ENERGIZED = 4
    HYPER = 5

    def _missing_(value):
        """Return the closest energy level for a given value when out of range."""
        if value < 1:
            return EnergyLevel.EXHAUSTED
        else:
            return EnergyLevel.HYPER

    def __str__(self):
        """Return a string representation of the energy level."""
        if self == EnergyLevel.EXHAUSTED:
            return "exhausted"
        elif self == EnergyLevel.TIRED:
            return "tired"
        elif self == EnergyLevel.NORMAL:
            return "normal"
        elif self == EnergyLevel.ENERGIZED:
            return "energized"
        else:
            return "HYPER"


class StressLevel(Enum):
    """Stress level palette of the machine."""
    CALM = 1
    NEUTRAL = 2
    NERVOUS = 3
    TENSE = 4
    STRESSED = 5
    RAGING = 6

    def _missing_(value):
        """Return the closest stress level for a given value when out of range."""
        if value < 1:
            return StressLevel.CALM
        elif value > 6:
            return StressLevel.RAGING
        else:
            return StressLevel(value)

    def __str__(self):
        """Return a string representation of the stress level."""
        if self == StressLevel.CALM:
            return "calm"
        elif self == StressLevel.NEUTRAL:
            return "neutral"
        elif self == StressLevel.NERVOUS:
            return "nervous"
        elif self == StressLevel.TENSE:
            return "tense"
        elif self == StressLevel.STRESSED:
            return "stressed"
        else:
            return "raging"


class Emotion(Enum):
    """Emotion palette of the machine."""
    Content = "content"
    Happy = "happy"
    Excited = "excited"
    Sad = "sad"
    Angry = "angry"
    Fearful = "fearful"
    Anxious = "anxious"
    Nostalgic = "nostalgic"
    Amused = "amused"
    Bored = "bored"
    Confused = "confused"
    Disgusted = "disgusted"
    Envious = "envious"
    Frustrated = "frustrated"
    Surprised = "surprised"


class Set(Enum):
    """Available scene sets the machine can run in."""
    HOME_LAB = "Vintage 1980 Z80 based Crown gambling machine sits in mysterious hackers home lab and being cared for, getting a new life."
    FURRY_HACKATHON = "Original vintage Th. Bergmann Automatenbau 1980 Crown gambling machine comes to life at a furry hackathon after collecting dust for 30 years."
    POSTAPOCALYPTIC = "How this vintage Crown gambling machine survived the apocalypse remains a mystery, yet here it is."
    CT2023 = "Fortune and mystery brought this vintage 1980 Th. Bergmann Crown automatenbau gambling machine to Cybertown 2023 LARP and music festival. Property of Vault tec."


class MachineBrain:
    instance = None
    event_queue = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def getStatus(self):
        """Returns state of the machine in form of prompt-compatible text."""
        return f"\nStatus: energy - {self.energy_level.name.lower()}, stress - {self.stress_level.name.lower()}, emotion - {self.emotion.value}.\n"

    def play_crown_sound(self):
        """Play the appropriate Crown sound intro based on the energy level."""
        if (self.energy_level == EnergyLevel.EXHAUSTED):
            self.play_audio_file(Path("media/Crown Intro 050 pct.wav"))
        elif (self.energy_level == EnergyLevel.TIRED):
            self.play_audio_file(Path("media/Crown Intro 050 pct.wav"))
        elif (self.energy_level == EnergyLevel.NORMAL):
            self.play_audio_file(Path("media/Crown Intro.wav"))
        elif (self.energy_level == EnergyLevel.ENERGIZED):
            self.play_audio_file(Path("media/Crown Intro 140 pct.wav"))
        elif (self.energy_level == EnergyLevel.HYPER):
            self.play_audio_file(Path("media/Crown Intro 200 pct.wav"))
        else:
            self.play_audio_file(Path("media/Crown Intro.wav"))

    def crown_play_audio(self, File_name):
        """Play an audio file with Crown sound intro."""
        self.play_crown_sound()
        self.play_audio_file(Path(config.AUDIO_CACHE_FOLDER, File_name))

    def play_audio_file(self, fileToPlay):
        """Play an audio file using pygame."""
        file = str(fileToPlay.resolve())
        logging.debug(f"Playing audio {file}")
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def brain_shuffle(self):
        """Shuffle the machine brain and set the machine to a random state."""
        self.energy_level = EnergyLevel(
            self.energy_level.value + random.randint(-1, 1))
        self.stress_level = random.choice(list(StressLevel))
        self.emotion = random.choice(list(Emotion))
        logging.debug(
            f"Machine Brain shuffled with {self.getStatus()}")

    def get_random_line_from_cache(self):
        """Get a random line from the audio cache."""
        cache_line = cache.select_random_text(Path(config.DATABASE_FILE))
        return cache_line

    def vocalize_text_line(self, text_line):
        file_name = cache.text_to_hash(text_line)+".wav"
        logging.debug(f"Attempting cached playback of {file_name}.")
        file_path = Path(config.AUDIO_CACHE_FOLDER, file_name)
        if not (file_path.is_file()):
            logging.warn(f"Cache miss! The file {file_path} doesn't exists.")
            googletts.download_audio(text_line)
        self.crown_play_audio(file_name)

    def vocalize_from_cache(self):
        """Vocalize a random line from the JSON/audio cache."""
        cache_line = cache.select_random_text()
        self.vocalize_text_line(cache_line)

    def vocalize_new(self):
        """Vocalize a new line using OpenAI and Google TTS and store it to audio cache."""
        prompt_input = f"{config.OPENAI_PROMPT_PROGRAM}Set: {self.set.value}{self.getStatus()}\nYou say:\n"
        # Prompt structure: Program - Set - Machine status - prompt:

        newline = openai.crown_generate_text(prompt_input, 50)

        cache.get_or_create_entry(newline)
        self.vocalize_text_line(newline)

    def startup(self):
        self.energy_level = EnergyLevel.NORMAL
        self.stress_level = StressLevel.CALM
        self.emotion = Emotion.Nostalgic
        self.set = Set.CT2023
        self.play_crown_sound()
        self.event_queue.add_event(Event(EventTypes.MACHINE_SLEEP, 10))
    
    def sleep(self, seconds):
        """Let the machine sleep for a given number of seconds."""
        logging.debug(f"Sleep. See you in {seconds} seconds.")
        time.sleep(seconds)

    def __init__(self):
        """Initialize the machine brain."""
        self.event_queue = EventQueue()
        self.event_queue.add_event(Event(EventTypes.MACHINE_STARTUP))
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        logging.debug("Machine Brain initialized.")
