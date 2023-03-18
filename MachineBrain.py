from enum import Enum
from pathlib import Path
import requests
import random
import logging
import config
import pygame
import cache
import crown_ai
import platform
import googletts
import time
from promptgenerator import PromptGenerator
from conversation import Conversation
from props.scenes import Scenes
from states.emotions import Emotions
from states.behaviors import Behavior
from states.energy import Energy
from states.stress import Stress
from datetime import datetime
from events import EventQueue, EventTypes, Event
from gpiozero import MotionSensor
from gpiozero.pins.mock import MockFactory


# This set of classes is the brain of the machine. It is responsible for the machine's state and behavior.
# The MachineBrain is a singleton class, so there can only be one instance of it at a time.


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
        return f"Your status is: energy - {self.energy_level.name.lower()}, stress - {self.stress_level.name.lower()}, emotion - {self.emotion.value}."

    def play_crown_sound(self):
        """Play the appropriate Crown sound intro based on the energy level."""
        if (self.energy_level == Energy.EXHAUSTED):
            self.play_audio_file(Path("media/Crown Intro 050 pct.wav"))
        elif (self.energy_level == Energy.TIRED):
            self.play_audio_file(Path("media/Crown Intro 050 pct.wav"))
        elif (self.energy_level == Energy.NORMAL):
            self.play_audio_file(Path("media/Crown Intro.wav"))
        elif (self.energy_level == Energy.ENERGIZED):
            self.play_audio_file(Path("media/Crown Intro 140 pct.wav"))
        elif (self.energy_level == Energy.HYPER):
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
        if (self.behavior_mode == Behavior.CRAZY):
            self.brain_shuffle()
        elif (self.behavior_mode == Behavior.NORMAL):
            self.brain_advance()
        else:
            return

    def brain_advance(self):
        """Advance the machine brain one step."""
        self.energy_level = Energy(
            self.energy_level.value + random.randint(-1, 1))
        self.stress_level = Stress(
            self.stress_level.value + random.randint(-1, 1))
        if (random.randint(0, 9) < 3):  # 30% chance of emotion change
            self.emotion = random.choice(list(Emotions))

        logging.debug(
            f"MB - advanced to {self.getStatus()}")

    def brain_shuffle(self):
        """Shuffle the machine brain and set the machine to a random state."""
        self.energy_level = random.choice(list(Energy))
        self.stress_level = random.choice(list(Stress))
        self.emotion = random.choice(list(Emotions))
        logging.debug(
            f"MB - shuffled to {self.getStatus()}")

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
                googletts.download_audio_czech(
                    text_line, SpeakingRate=googletts.energy_enum_to_speaking_rate(self.energy_level))
            else:
                googletts.download_audio(text_line)

        self.crown_play_audio(file_name)

    def vocalize_from_cache(self):
        """Vocalize a random line from the JSON/audio cache."""
        cache_line = cache.select_random_text()
        self.vocalize_text_line(cache_line)

    def vocalize_random(self, event=None):
        if self.online:
            choice = random.randint(0, 2)
            PG = PromptGenerator()
            self.conversation = Conversation().with_default_messages()
            if choice == 0:
                self.conversation = (PG.with_get_single_life_anecdote(self.conversation, self.emotion.value,
                                     96, None, Scenes.CT2023, self.getStatus()))
            elif choice == 1:
                self.conversation = (PG.with_get_single_life_anecdote_with_random_props(self.conversation, self.emotion.value,
                                                                                        256, None, Scenes.CT2023, self.getStatus()))
            else:
                self.conversation = (PG.with_get_single_vault_tec_praise(self.conversation, self.emotion.value,
                                                                         72, None, Scenes.CT2023, self.getStatus()))

            self.conversation = self.conversation.with_message(
                "user", "You continue in Czech: ")
            self.conversation = crown_ai.advance_conversation(
                self.conversation)

            memory_text = self.conversation.get_last_assistant_message()
            logging.debug(f"MB - New Text Line: {memory_text}")
            cache.get_or_create_entry(
                memory_text, self.getStatusObject(), event)
            self.vocalize_text_line(memory_text)
        else:
            self.vocalize_from_cache()

    def vocalize_direct(self, text, cache=True, event=None):
        """Vocalize a given line using Google TTS."""
        if (cache):
            cache.get_or_create_entry(text, self.getStatusObject(), event)
        self.vocalize_text_line(text)

    def vocalize_current_time(self, event=None):
        """Vocalize the current time."""
        cd = datetime.now()
        hours = cd.strftime("%H")
        minutes = cd.strftime("%M")
        if (config.LANGUAGE == "Czech"):
            self.vocalize_direct(
                f"Právě je {hours} hodin a {minutes} minut.", False, event)
        else:
            self.vocalize_direct(
                f"Current time is {hours} hours and {minutes} minutes.", False, event)

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
        self.behavior_mode = Behavior.NORMAL
        self.wake_up = False
        self.recent_motion = datetime.now()
        self.online = self.check_connection_is_online()
        self.energy_level = Energy.NORMAL
        self.stress_level = Stress.CALM
        self.emotion = Emotions.Nostalgic
        self.set = Scenes.CT2023
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
