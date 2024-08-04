# CrownPiBot / CrownPyBot

A talking machine project based on a vintage 1980 Th. Bergmann Automatenbau Crown gambling machine, Raspberry Pi Zero W, OpenAI API and Google Cloud Text To Speech. If you want more information about the original machine, check [Wolf's Sammler - Seite zu Bergmann -CROWN- und anderen Spielautomaten](http://www.baersch-online.de/spielautm.htm).

## Requirements

- Raspberry Pi (Zero W or better)
- Up to date Raspbian OS installed
- Python 3
- Git
- An API key for OpenAI API
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

### New Hardware

- Add PIR Sensor [WIP]
- Add Microphone
- Add RPI Camera
- Add LEDs, display or terminal

### CrownPyBot RPi Project
- Change JSON to SQLite[✔️]
- Change OG Completions model to chat based GPT-4o [✔️]
- Develop entertaining self propelled machine loop [WIP]
- Add Telegram bot [WIP]
- Extend story telling capabilities
- Extend audio / scenario / content / props ...
- Web interface, weather, location, ...?



# Machine Hardware Description and Control Plan

## Components Overview

1. **220V Motors (3x)**:
   - **Function**: Spin the wheels.
   - **Control**: Relays controlled by ESP32.

2. **Spinning Wheel Photoresistors (3x)**:
   - **Function**: Detect the status of the spinning wheels.
   - **Control**: Analog inputs on ESP32.

3. **7-Segment Displays (3x LEFT, 4x RIGHT)**:
   - **Function**: Display numbers.
   - **Control**: Multiplexed control using GPIOs on ESP32, possibly using a 7-segment driver IC like MAX7219 for simplicity.

4. **Bulbs/LEDs (10x LEFT, 10x RIGHT, 8x Central, SUPERCHANCE, SONDERSPIELE, Coin Entry)**:
   - **Function**: Indicate various statuses and game phases.
   - **Control**: GPIOs on ESP32.

5. **Buttons (Risiko LEFT/RIGHT, START, STOP Center/Right, Pay Winning)**:
   - **Function**: User input.
   - **Control**: GPIOs on ESP32, with debouncing in software(?).