# CrownPiBot

A talking machine project based on Raspberry Pi Zero W and OpenAI GPT-3 API.

## Requirements

- Raspberry Pi (Zero W or better)
- Up to date Raspbian OS installed
- Python 3
- Git
- An API key for OpenAI GPT-3 API
- "Credentials" for Google Text-to-Speech API

## Setup

1. Clone the repository to your Raspberry Pi:

    git clone https://github.com/your_username/CrownPiBot.git

2. Install the required packages:

    pip install -r requirements.txt

3. Replace the placeholder API keys in `config.py` with your own API keys.

4. Run the program:

    python main.py

## Autostart

## Optional

- Check this guide if you have a need for BT audio: https://gist.github.com/actuino/9548329d1bba6663a63886067af5e4cb
- Run the bot at system startup as a service: https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6