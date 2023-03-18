from conversation import Conversation
from enum import Enum
import random
import logging
import tiktoken
from states.emotions import Emotions
from props.eras import Eras
from props.locations import Locations
from props.characters import Characters
from props.objects import Objects
from props.scenes import Scenes
from conversation import Conversation


class PromptGenerator:
    """A class that assists in prompt construction."""

    def generate_props_showcase_message(self, emotion=Emotions.Happy.value):
        """Generate a single conversation message containing an AI prompt showcasing our props enums."""
        message = f"You tell a short {emotion} anecdote. Location? { Locations.random().value} Time? {  Eras.random().value }"
        logging.debug(f"PG - props_showcase - {message}")
        return Conversation.create_message("user", message)

    def generate_praise_vault_tec_message(self):
        """Generate a prompt praising Vault-Tec."""
        message = f"You greet passer-bys with an over the top post apocalyptic funny punchline about Vault-tec [Valtek]."
        return Conversation.create_message("user", message)

    def generate_random_props_string(self):
        number_of_eras = random.randint(0, 2)
        number_of_locations = random.randint(0, 2)
        number_of_characters = random.randint(0, 4)
        number_of_objects = random.randint(0, 4)
        result_string = ""

        for i in range(number_of_eras):
            result_string += f"{random.choice(list(Eras)).value} "
        for i in range(number_of_locations):
            result_string += f"{random.choice(list(Locations)).value} "
        for i in range(number_of_characters):
            result_string += f"{random.choice(list(Characters)).value} "
        for i in range(number_of_objects):
            result_string += f"{random.choice(list(Objects)).value} "

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        logging.debug(
            f"AI - props weight - Pr-{len(encoding.encode(result_string))} tokens.")
        return result_string

    def with_get_single_life_anecdote(self, Conversation, Word_Count=128, Context=None, Scene=None, Status=None) -> 'Conversation':
        Conversation.with_default_messages(Context, Scene, Status)
        Conversation.with_message(
            "user", f"Tell a shorter than {Word_Count} word anecdote from you life.")
        return Conversation

    def with_get_single_life_anecdote_with_random_props(self, Conversation, Emotion, Word_Count=256, Context=None, Scene=None, Status=None) -> 'Conversation':
        PG = PromptGenerator()
        random_props_string = PG.generate_random_props_string()
        Conversation.with_default_messages(Context, Scene, Status)
        Conversation.with_message(
            "user", f"Tell a {Word_Count} words long {Emotion} story from you life. Adopt the following props: {random_props_string}.")
        return Conversation

    def with_get_single_vault_tec_praise(self, Conversation, Word_Count=128, Context=None, Scene=None, Status=None) -> 'Conversation':
        Conversation.with_default_messages(Context, Scene, Status)
        Conversation.with_message(
            "user", f"Tell a shorter than {Word_Count} word unexpected and funny Vault-Tek praise.")
        return Conversation
