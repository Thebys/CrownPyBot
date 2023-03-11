import json
import config
import requests
import logging
import config


def crown_generate_text(Prompt_Input, Max_Tokens=20, temperature=0.65, top_p=0.8):
    """Return new text line from the AI model, based on the prompt input."""
    logging.debug(f"AI - Prompt: {Prompt_Input}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.OPENAI_API_KEY}"
    }
    data = {
        "prompt": Prompt_Input,
        "model": config.OPENAI_AI_MODEL,
        "temperature": temperature,
        "max_tokens": Max_Tokens,
        "top_p": top_p,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    response = requests.post(
        config.OPENAI_API_ENDPOINT,
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
