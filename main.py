import logging
import random
import time
import config
import MachineBrain
from MachineBrain import Set
from MachineBrain import Setting
from MachineBrain import MachineBrain


def pause(seconds=random.randint(15, 30)):
    pause = seconds
    logging.debug(f"Sleep. See you in {pause} seconds.")
    time.sleep(pause)


def setup():
    logging.basicConfig(filename="CrownPiBot.log", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.debug("Setup started.")
    MachineBrain()


def loop():
    while (True):
        process_round()


def process_round():
    CrownBotBrain = MachineBrain.instance
    setting = CrownBotBrain.getSetting()
    if setting == Setting.STARTING_UP:
        CrownBotBrain.play_intro_modem()
        CrownBotBrain.setting = Setting.IDLE
    elif setting == Setting.IDLE:
        bored = random.randint(0, 99)
        if (bored > 88 and config.LEARNING):
            CrownBotBrain.vocalizeNew()
        else:
            CrownBotBrain.vocalizeFromCache()
            CrownBotBrain.brain_shuffle()
        pause()
    else:
        CrownBotBrain.vocalizeFromCache()
        CrownBotBrain.brain_shuffle()
        pause()


def main():
    setup()
    loop()


if __name__ == "__main__":
    main()
