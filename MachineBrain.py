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


class EnergyLevel(Enum):
    EXHAUSTED = 1
    TIRED = 2
    NORMAL = 3
    ALERT = 4
    ENERGIZED = 5
    HYPER = 6

    def __str__(self):
        if self == EnergyLevel.EXHAUSTED:
            return "exhausted"
        elif self == EnergyLevel.TIRED:
            return "tired"
        elif self == EnergyLevel.NORMAL:
            return "normal"
        elif self == EnergyLevel.ALERT:
            return "alert"
        elif self == EnergyLevel.ENERGIZED:
            return "energized"
        else:
            return "hyper"


class StressLevel(Enum):
    CALM = 1
    NEUTRAL = 2
    NERVOUS = 3
    TENSE = 4
    STRESSED = 5
    RAGING = 6

    def __str__(self):
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


class Set(Enum):  # Scene and its description is…
    HOME_LAB = "Vintage 1980 Z80 based Crown gambling machine sits in mysterious hackers home lab and being cared for, getting a new life."
    FURRY_HACKATHON = "Original vintage Th. Bergmann Automatenbau 1980 Crown gambling machine comes to life at a furry hackathon after collecting dust for 30 years."
    POSTAPOCALYPTIC = "How this vintage Crown gambling machine survived the apocalypse remains a mystery, yet here it is."
    CT2023 = "Fortune and mystery have brought this vintage 1980 Th. Bergmann Crown automatenbau gambling machine to Cybertown 2023 LARP and music festival. Property of Vault tec."


class Setting(Enum):  # Current sittuation and attention span focus
    STARTING_UP = "The machine starts up."
    IDLE = "The machine is idle."
    ATTENTION_SEEKING = "The machine seeks attention."
    BYSTANDER_LOOKING = "The machine observes a bystander."
    GROUP_OF_BYSTANDERS = "The machine observes a group of bystanders."
    NEW_GAME = "The machine starts a new game."
    PLAYER_WINNING = "The machine player is winning."
    PLAYER_LOOSING = "The machine player is loosing."
    MACHINE_ERROR = "The machine throws an error!"
    BORED = "The machine is bored."


class PromptTemplates(Enum):
    # Set / Energy level / stress level / emotion -> punch line
    STARTUP = "{0} The machine starts up with {1} energy level and {2} stress level. The machine is {3}. It says this punch line:"
    # Set / Energy level / stress level / emotion -> punch line
    SEEK_ATTENTION = "{0} The machine seeks attention with {1} energy level and {2} stress level. The machine is {3}. It says this punch line:"
    # Set / Energy level / stress level / emotion -> punch line
    BORED = "{0} The machine is {3} and bored after period of no interaction. Its energy level is {1} and its stress level is {2}. It shortly comments the situation:"


class MachineBrain:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def getSetting(self):
        return self.setting

    def getStatus(self):
        return "\nMachine status: energy - {0}, stress - {1}, emotion - {2}.\n".format(self.energy_level.name.lower(), self.stress_level.name.lower(), self.emotion.value)
    
    def play_intro_modem(self):
        self.play_audio_file(Path("media/Crown Intro.wav"))         

    def crown_play_audio(self, File_name):
        self.play_audio_file(Path("media/Crown Intro.wav"))
        self.play_audio_file(Path(config.AUDIO_CACHE_FOLDER, File_name))

    def play_audio_file(self, fileToPlay):
        file = str(fileToPlay.resolve())
        logging.debug(f"Playing audio {file}")
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def brain_shuffle(self):
        self.energy_level = random.choice(list(EnergyLevel))
        self.stress_level = random.choice(list(StressLevel))
        self.emotion = random.choice(list(Emotion))
        self.setting = random.choice(list(Setting))
        logging.debug(
            f"Machine Brain shuffled with {self.getStatus()} and setting: {self.setting.name}")

    def vocalizeFromCache(self):
        cache_line = cache.select_random_text(Path(config.DATABASE_FILE))
        file_name = cache.text_to_hash(cache_line)+".wav"
        logging.debug("Vocalizing file {0} from cache with text: {1}.".format(
            file_name, cache_line))
        file_path = Path(config.AUDIO_CACHE_FOLDER, file_name)
        if not (file_path.is_file()):
            logging.error(
                f"Cache miss! Database file likely corrupted. The file {file_path} doesn't exists.")
        self.crown_play_audio(file_name)

    def vocalizeNew(self):
        # Program - Set - Machine status - Setting - prompt:
        prompt_input = f"{config.OPENAI_PROMPT_PROGRAM}Set: {self.set.value}{self.getStatus()}Setting: {self.setting.value}\nIt says:\n"
        newline = openai.crown_generate_text(prompt_input, 50)

        file_name = cache.text_to_hash(newline)+".wav"
        file_path = Path(config.AUDIO_CACHE_FOLDER, file_name)
        cache.get_or_create_entry(Path(config.DATABASE_FILE), newline)
        if not (file_path.is_file()):
            logging.warn(f"Cache miss! The file {file_path} doesn't exists.")
            googletts.download_audio(newline)
            self.crown_play_audio(file_name)

    def __init__(self, Energy=EnergyLevel.ENERGIZED, Stress=StressLevel.CALM, Emotion=Emotion.Content, Set=Set.CT2023):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        self.energy_level = Energy
        self.stress_level = Stress
        self.emotion = Emotion
        self.set = Set
        self.setting = Setting.STARTING_UP
        logging.debug("Machine Brain initialized.")
