import json
import config
import requests
import logging
import config
    
def crown_generate_text(Prompt_Input, Max_Tokens = 20):
    logging.debug("AI request prompt:\n{0}".format(Prompt_Input))
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.OPENAI_API_KEY}"
    }
    data = {
        "prompt": Prompt_Input,
        "model": config.OPENAI_AI_MODEL,
        "temperature": 0.5,
        "max_tokens": Max_Tokens,
        "top_p": 1,
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
        logging.debug("AI request response::\{0}".format(response_newtextline))
        return response_newtextline
    else:
        logging.error(f"Failed to generate text: {response.content}")