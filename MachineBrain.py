from enum import Enum
from pathlib import Path
import requests
import random
import logging
import config
import pygame
import cache
import openai
import platform
import googletts
import time
import PromptGenerator
from datetime import datetime
from events import EventQueue, EventTypes, Event
from gpiozero import MotionSensor
from gpiozero.pins.mock import MockFactory


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
    Excited = "excited"
    Surprised = "surprised"
    Happy = "happy"
    Content = "content"
    Amused = "amused"
    Nostalgic = "nostalgic"
    Angry = "angry"
    Sad = "sad"
    Fearful = "fearful"
    Anxious = "anxious"
    Bored = "bored"
    Confused = "confused"
    Disgusted = "disgusted"
    Envious = "envious"
    Frustrated = "frustrated"


class BehaviorMode(Enum):
    """Available behavior modes the machine can run in."""
    CALM = "calm"
    NORMAL = "normal"
    CRAZY = "crazy"


class Set(Enum):
    """Available scene sets the machine can run in."""
    HOME_LAB = "Vintage 1980 Z80 based Crown gambling machine sits in mysterious hackers home lab and being cared for, getting a new life."
    FURRY_HACKATHON = "Original vintage Th. Bergmann Automatenbau 1980 Crown gambling machine comes to life at a furry hackathon after collecting dust for 30 years."
    POSTAPOCALYPTIC = "How this vintage Crown gambling machine survived the apocalypse remains a mystery, yet here it is."
    CT2023 = "Fortune and mystery brought you to Cybertown 2023 LARP and music festival. You roleplay a vending machine and are a proud property of Vault tec faction."


class MachineBrain:
    """The brain of the machine. It is responsible for the machine's state and behavior."""
    instance = None
    event_queue = None
    behavior_mode = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def getStatusObject(self):
        """Returns state of the machine in form of a dictionary."""
        return {"energy": self.energy_level.value, "stress": self.stress_level.value, "emotion": self.emotion.value}

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
        logging.debug(f"FS - Playing audio {file}")
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def advance(self):
        """Advance the machine state by one step based on selected behavior mode."""
        if (self.behavior_mode == BehaviorMode.CRAZY):
            self.brain_shuffle()
        elif (self.behavior_mode == BehaviorMode.NORMAL):
            self.brain_advance()
        else:
            return

    def brain_advance(self):
        """Advance the machine brain one step."""
        self.energy_level = EnergyLevel(
            self.energy_level.value + random.randint(-1, 1))
        self.stress_level = StressLevel(
            self.stress_level.value + random.randint(-1, 1))
        if (random.randint(0, 9) < 3):  # 30% chance of emotion change
            self.emotion = random.choice(list(Emotion))

        logging.debug(
            f"Machine Brain advanced to {self.getStatus()}")

    def brain_shuffle(self):
        """Shuffle the machine brain and set the machine to a random state."""
        self.energy_level = random.choice(list(EnergyLevel))
        self.stress_level = random.choice(list(StressLevel))
        self.emotion = random.choice(list(Emotion))
        logging.debug(
            f"Machine Brain shuffled to {self.getStatus()}")

    def get_random_line_from_cache(self):
        """Get a random line from the audio cache."""
        cache_line = cache.select_random_text(Path(config.DATABASE_FILE))
        return cache_line

    def vocalize_text_line(self, text_line):
        file_name = cache.text_to_hash(text_line)+".wav"
        logging.debug(f"FS - Attempting cached playback of {file_name}.")
        file_path = Path(config.AUDIO_CACHE_FOLDER, file_name)
        if not (file_path.is_file()):
            logging.warn(
                f"FS - Cache miss! The file {file_path} doesn't exists.")
            if (config.LANGUAGE == "Czech"):
                energy_based_speaking_rate = 0.95
                if self.energy_level == EnergyLevel.EXHAUSTED:
                    energy_based_speaking_rate = 0.75
                elif self.energy_level == EnergyLevel.TIRED:
                    energy_based_speaking_rate = 0.85
                elif self.energy_level == EnergyLevel.NORMAL:
                    energy_based_speaking_rate = 0.95
                elif self.energy_level == EnergyLevel.ENERGIZED:
                    energy_based_speaking_rate = 1.15
                elif self.energy_level == EnergyLevel.HYPER:
                    energy_based_speaking_rate = 1.30
                googletts.download_audio_czech(
                    text_line, SpeakingRate=energy_based_speaking_rate)
            else:
                googletts.download_audio(text_line)

        self.crown_play_audio(file_name)

    def vocalize_from_cache(self):
        """Vocalize a random line from the JSON/audio cache."""
        cache_line = cache.select_random_text()
        self.vocalize_text_line(cache_line)

    def vocalize_new(self, event=None):
        """Vocalize a new line using OpenAI and Google TTS and store it to audio cache."""
        if config.LANGUAGE == "Czech":
            if event is not None:
                prompt_input = f"{config.OPENAI_PROMPT_PROGRAM_CZECH}Scene: {self.set.value}{self.getStatus()}{str(event.type)} You say:\n"
            else:
                prompt_input = f"{config.OPENAI_PROMPT_PROGRAM_CZECH}Scene: {self.set.value}{self.getStatus()}You say:\n"
        else:
            if event is not None:
                prompt_input = f"{config.OPENAI_PROMPT_PROGRAM}Scene: {self.set.value}{self.getStatus()}{str(event.type)} You say:\n"
            else:
                prompt_input = f"{config.OPENAI_PROMPT_PROGRAM}Scene: {self.set.value}{self.getStatus()}You say:\n"
        newline = openai.crown_generate_text(prompt_input, 50)
        cache.get_or_create_entry(newline, self.getStatusObject(), event)
        self.vocalize_text_line(newline)

    def vocalize_random_memory(self, event=None):
        if self.online:
            self.vocalize_new_random_memory(event)
        else:
            self.vocalize_from_cache()

    def vocalize_new_random_memory(self, event=None):
        """Vocalize new random memory using prompt generator, OpenAI and Google TTS and store it to audio cache."""
        PG = PromptGenerator.PromptGenerator()
        if config.LANGUAGE == "Czech":
            prompt = f"{config.OPENAI_PROMPT_PROGRAM_CZECH}Scene: {self.set.value}{self.getStatus()}{PG.generate_random_memory_prompt(self.emotion.value)} You say:\n"
        else:
            prompt = f"{config.OPENAI_PROMPT_PROGRAM}Scene: {self.set.value}{self.getStatus()}{PG.generate_random_memory_prompt(self.emotion.value)} You say:\n"
        memory_text = openai.crown_generate_text(prompt, 2000, 0.9, 0.65)
        cache.get_or_create_entry(memory_text, self.getStatusObject(), event)
        self.vocalize_text_line(memory_text)

    def vocalize_praise_vault_tec(self, event=None):
        """Vocalize a praise for Vault-Tec using Google TTS."""
        PG = PromptGenerator.PromptGenerator()
        if config.LANGUAGE == "Czech":
            prompt = f"{config.OPENAI_PROMPT_PROGRAM_CZECH}Scene: {self.set.value}{self.getStatus()}{PG.praise_vault_tec()} You say:\n"
        else:
            prompt = f"{config.OPENAI_PROMPT_PROGRAM}Scene: {self.set.value}{self.getStatus()}{PG.praise_vault_tec()} You say:\n"
        praise_text = openai.crown_generate_text(prompt, 1200, 0.95, 0.35)
        self.vocalize_text_line(praise_text)

    def vocalize_direct(self, text, event=None):
        """Vocalize a given line using Google TTS."""
        cache.get_or_create_entry(text, self.getStatusObject(), event)
        self.vocalize_text_line(text)

    def vocalize_current_time(self, event=None):
        """Vocalize the current time."""
        cd = datetime.now()
        hours = cd.strftime("%H")
        minutes = cd.strftime("%M")
        if (config.LANGUAGE == "Czech"):
            self.vocalize_direct(
                f"Pr??v?? je {hours} hodin a {minutes} minut.", event)
        else:
            self.vocalize_direct(
                f"Current time is {hours} hours and {minutes} minutes.", event)

    def check_connection_is_online(self):
        """Check if the internet connection is online."""
        try:
            req = requests.head("https://google.com", timeout=5)
            # HTTP errors are not raised by default, this statement does that
            req.raise_for_status()
            return True
        except requests.HTTPError as e:
            logging.warn(
                f"CON - Checking internet connection failed, status code {e.response.status_code}")
        except requests.ConnectionError:
            logging.warn("CON - No internet connection available.")
        self.stress_level = + 1
        return False

    def startup(self):
        """Start the machine and set it to a default state."""
        if (platform.system() == "Windows"):  # Windows DEV has no real GPIO
            PF = MockFactory()
            # MOCK PIN, see https://gpiozero.readthedocs.io/en/stable/api_pins.html#mock-pins
            self.pir = MotionSensor(4, pin_factory=PF)
        else:
            self.pir = MotionSensor(4)  # GPIO pin 4 (physical pin 7)
        self.pir.when_motion = self.motion_detected
        self.behavior_mode = BehaviorMode.NORMAL
        self.wake_up = False
        self.recent_motion = datetime.now()
        self.online = self.check_connection_is_online()
        self.energy_level = EnergyLevel.NORMAL
        self.stress_level = StressLevel.CALM
        self.emotion = Emotion.Nostalgic
        self.set = Set.CT2023
        if self.online:
            self.startup_online()
        else:
            self.startup_offline()

    def startup_online(self):
        self.play_crown_sound()
        self.event_queue.add_event(Event(EventTypes.MACHINE_SLEEP, 5))

    def startup_offline(self):
        self.play_crown_sound()
        self.event_queue.add_event(Event(
            EventTypes.DIRECT_SPEECH, "Hello, I am a vintage Crown gambling machine made by T H Bergmann in 1980."))
        self.event_queue.add_event(Event(EventTypes.MACHINE_SLEEP, 3))
        self.event_queue.add_event(Event(
            EventTypes.DIRECT_SPEECH, "I have been found, claimed and repaired by a mysterious hacker who saved me from 30 years stuck with a flat hoarder."))
        self.event_queue.add_event(Event(EventTypes.MACHINE_SLEEP, 5))
        self.event_queue.add_event(Event(EventTypes.SAY_TIME))
        self.event_queue.add_event(Event(EventTypes.MACHINE_SLEEP, 10))

    def motion_detected(self):
        """Handle motion detection HW event."""
        logging.debug("PIR - Motion detected!")
        self.recent_motion = datetime.now()
        self.wake_up = True
        if (self.event_queue.has_event_of_type(EventTypes.INPUT_PIR_DETECTED)):
            logging.debug("PIR - Motion already queued!")
            logging.debug(
                f"EQ - There are {self.event_queue.events.count()} total events.")
            return
        else:
            self.event_queue.add_event(Event(EventTypes.INPUT_PIR_DETECTED))

    def handle_movement(self, event=None):
        """Handle movement event from the EQ."""
        if ((datetime.now() - self.recent_motion).total_seconds() < 60):
            self.event_queue.add_event(Event(
                EventTypes.DIRECT_SPEECH, "Ah! Movement in infrared spectrum!"))

    def sleep(self, seconds=20):
        """Let the machine sleep for a given number of seconds."""
        logging.debug(f"EQ - Sleep. See you in {seconds} seconds.")
        for i in range(seconds):
            if self.wake_up:
                self.wake_up = False
                return
            else:
                time.sleep(1)

    def __init__(self):
        """Initialize the machine brain."""
        self.event_queue = EventQueue()
        self.event_queue.add_event(Event(EventTypes.MACHINE_STARTUP))
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)
        logging.debug("Machine Brain initialized.")
