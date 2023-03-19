# CrownPiBot / CrownPyBot

A talking machine project based on a vintage 1980 Th. Bergmann Automatenbau Crown gambling machine, Raspberry Pi Zero W, OpenAI API and Google Cloud Text To Speech. If you want more information about the original machine, check [Wolf's Sammler - Seite zu Bergmann -CROWN- und anderen Spielautomaten](http://www.baersch-online.de/spielautm.htm).

## Requirements

- Raspberry Pi (Zero W or better)
- Up to date Raspbian OS installed
- Python 3
- Git
- An API key for OpenAI GPT-3 API
- "Credentials" for Google Text-to-Speech API

## Setup

1. Clone the repository to your Raspberry Pi:

    `git clone https://github.com/your_username/CrownPiBot.git`

2. Install the required packages:

    `pip install -r requirements.txt`

3. Replace the placeholder API keys in `config.py` with your own API keys.

4. Run the program:

    `python main.py`


### Autostart

- Run the bot at system startup as a service: https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6

### Optional

- Check this guide if you have a need for BT audio: https://gist.github.com/actuino/9548329d1bba6663a63886067af5e4cb


## Roadmap / Tech tree

### OG Hardware

- Connect Parasite to original audio amplifier [WIP]
- Original / parasite mode switch / awareness
- Read Munzspeicher and Sonderspiele
- Read and handle original buttons

### New Hardware

- Add PIR Sensor [WIP]
- Add Microphone
- Add RPI Camera
- Add LEDs, display or terminal

### CrownPyBot RPi Project

- Add Telegram bot [WIP]
- Develop entertaining self propelled machine loop [WIP]
- Extend story telling capabilities
- Extend audio / scenario / content / props ...
- Web interface, weather, location, ...?
