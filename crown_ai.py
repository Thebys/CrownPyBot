import config
import logging
import config
import openai

def advance_conversation(Conversation, Max_Completion_Tokens=4096, Temperature=0.25, Top_p=0.9):
    '''Return a new chat message from the AI model, based on the Conversation.'''

    openai.api_key = config.OPENAI_API_KEY
    expected_length = Conversation.get_token_length() + Max_Completion_Tokens

    if (expected_length > config.OPENAI_CHAT_MODEL_MAX_TOKENS):
        logging.error(
            f"AI - Conversation + prompt = ({expected_length}) tokens is over AI model limit ({config.OPENAI_CHAT_MODEL_MAX_TOKENS}).")
        return Conversation
    else:
        ai_response = openai.chat.completions.create(
            model=config.OPENAI_CHAT_MODEL,
            max_tokens=Max_Completion_Tokens,
            temperature=Temperature,
            top_p=Top_p,
            messages=Conversation.get_messages(),
            stop=["translation", "Translation", "was"]
        )

        logging.debug(
            f'AI - Conversation advance finish reason - {ai_response.choices[0].finish_reason}.')
        logging.debug(
            f'AI - Conversation advance used P-{ai_response.usage.prompt_tokens} C-{ai_response.usage.completion_tokens} T-{ai_response.usage.total_tokens} tokens.')
        return Conversation.add_message({"role": "assistant", "content": ai_response.choices[0].message.content})
