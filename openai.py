import json
import config
import requests
import logging

def generate_text(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.OPENAI_API_KEY}"
    }
    data = {
        "prompt": prompt,
        "model": config.OPENAI_AI_MODEL,
        "temperature": 0.5,
        "max_tokens": 20,
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
        return response_json["choices"][0]["text"].strip().replace("'","").replace('"',"")
    else:
        logging.error(f"Failed to generate text: {response.content}")