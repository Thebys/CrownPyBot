import logging
import tiktoken
import config
import random
from enum import Enum
from props.scenes import Scenes
from props.eras import Eras
from props.locations import Locations
from props.characters import Characters
from props.objects import Objects


class Conversation:
    '''A class that represents a conversation between the user and the AI model.
        - messages: a list of messages, each message is a dict with keys "role" and "content"
        - token_length: the total number of tokens in the conversation
        - Initialy, the conversation is empty. Apply .with_default_messages() to add a default conversation.
        '''

    def __init__(self, messages=None):
        if messages is None:
            messages = []
        self.messages = messages
        self.token_length = 0
        self.refresh_token_length()

    def create_message(self, role, message):
        return {"role": role, "content": message}

    def with_default_messages(self, Context=None, Scene=None, Status=None) -> 'Conversation':
        if Context is None:
            context = config.CONTEXT_HISTORY
        else:
            context = Context

        if Scene is None:
            scene = Scenes.HOME_LAB.value
        else:
            scene = Scene.value

        if Status is None:
            status = "You are in a good mood."
        else:
            status = Status

        return (self.with_program()
                .with_message("user", context)
                .with_message("user", scene)
                .with_message("user", status))

    def with_program(self, program=None) -> 'Conversation':
        if program is None:
            program = config.OPENAI_PROMPT_PROGRAM_CZECH
        self.add_message(self.create_message("system", program))

        # Delete the following line after OpenAI fixes system prompts weight
        self.add_message(self.create_message("user", program))

        return self

    def with_message(self, role, message) -> 'Conversation':
        self.add_message(self.create_message(role, message))
        return self

    def add_message(self, message):
        self.messages.append(message)
        self.refresh_token_length()
        return self

    def get_messages(self):
        return self.messages

    def get_last_assistant_message(self):
        for message in reversed(self.messages):
            if message['role'] == 'assistant':
                return message['content']
        return None

    def get_token_length(self):
        self.refresh_token_length()
        return self.token_length

    def refresh_token_length(self, messages=None):
        if messages is None:
            messages = self.messages
        encoding = tiktoken.encoding_for_model("gpt-4o")
        self.token_length = 0
        messages_string = ''
        for message in messages:
            messages_string += message['role'] + message['content']
        self.token_length = len(encoding.encode(messages_string))
        logging.debug(
            f"AI - Tiktoken - Conversation has {len(messages)} msgs and total token length: T-{self.token_length} tokens.")
        return self.token_length
