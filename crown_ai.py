import json
import config
import requests
import logging
import config
import openai
import time
import tiktoken


def crown_gpt3_generate_text(Prompt_Input, Max_Tokens=20, temperature=0.65, top_p=0.8):
    """Return new text line from the AI model, based on the prompt input."""
    logging.debug(f"AI - Prompt: {Prompt_Input}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.OPENAI_API_KEY}"
    }
    data = {
        "prompt": Prompt_Input,
        "model": config.OPENAI_COMPLETIONS_MODEL,
        "temperature": temperature,
        "max_tokens": Max_Tokens,
        "top_p": top_p,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    response = requests.post(
        config.OPENAI_API_COMPLETIONS_ENDPOINT,
        headers=headers,
        data=json.dumps(data)
    )
    if response.status_code == 200:
        response_json = response.json()
        response_newtextline = response_json["choices"][0]["text"].strip()
        logging.debug(f"AI - Response: {response_newtextline}")
        return response_newtextline
    else:
        logging.error(f"Failed to generate text: {response.content}")


def crown_ai_conversation():
    '''Perform a conversation using the AI model.'''
    messages = [
        {"role": "system", "content": config.OPENAI_PROMPT_PROGRAM_CZECH},
        # TODO: remove this v line, Current workaround for OpenAI weak system prompts
        {"role": "user", "content": config.OPENAI_PROMPT_PROGRAM_CZECH},
        {"role": "user", "content": "Tell a story about yourself."}]

    conversation = Conversation(messages=messages)
    conversation = conversation.add_message(
        crown_ai_advance_conversation(conversation.get_messages()))
    # for each message print a debug line
    for message in conversation.get_messages():
        if (message['role'] == "assistant" or config.DEVELOPMENT == True):
            logging.debug(
                f"AI - Conversation - R:{message['role']} C:{message['content']}")
    return conversation


def crown_ai_advance_conversation(Messages, Max_Tokens=360, Temperature=0.2, Top_p=0.6):
    '''Return a new chat message from the AI model, based on the messages.'''
    openai.api_key = config.OPENAI_API_KEY

    ai_response = openai.ChatCompletion.create(
        model=config.OPENAI_CHAT_MODEL,
        max_tokens=Max_Tokens,
        temperature=Temperature,
        top_p=Top_p,
        messages=Messages
    )

    logging.debug(
        f'AI - Finish reason - {ai_response["choices"][0]["finish_reason"]}.')
    logging.debug(
        f'AI - This AI exchange used P-{ai_response["usage"]["prompt_tokens"]} C-{ai_response["usage"]["completion_tokens"]} T-{ai_response["usage"]["total_tokens"]} tokens.')
    return ai_response["choices"][0]["message"]


class Conversation:
    def __init__(self, messages):
        self.messages = messages
        self.token_length = 0
        self.refresh_token_length()

    def add_message(self, message):
        self.messages.append(message)
        self.refresh_token_length()
        return self

    def get_messages(self):
        return self.messages

    def get_token_length(self):
        self.refresh_token_length()
        return self.token_length

    def refresh_token_length(self, messages=None):
        if messages is None:
            messages = self.messages
        encoding = tiktoken.get_encoding("cl100k_base")
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.token_length = 0
        messages_string = ''
        for message in messages:
            messages_string += message['role'] + message['content']
        self.token_length = len(encoding.encode(messages_string))
        logging.debug(
            f"AI - Tiktoken - Conversation token length: T-{self.token_length} tokens.")
        return self.token_length
