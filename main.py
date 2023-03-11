import logging
import random
import time
import config
import MachineBrain
from MachineBrain import Set
from MachineBrain import Setting
from MachineBrain import MachineBrain


def pause(seconds=20):
    """Let the machine sleep for a given number of seconds."""
    logging.debug(f"Sleep. See you in {seconds} seconds.")
    time.sleep(seconds)


def setup():
    """Setup the machine."""
    logging.basicConfig(filename="CrownPiBot.log", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.debug("Setup started.")
    MachineBrain()


def loop():
    """Loop the machine's life."""
    while (True):
        process_round()


def process_round():
    """Process a round of the machine's life."""
    CrownBotBrain = MachineBrain.instance
    setting = CrownBotBrain.getSetting()
    if setting == Setting.STARTING_UP:
        CrownBotBrain.play_crown_sound()
        CrownBotBrain.setting = Setting.IDLE
    elif setting == Setting.IDLE:
        bored = random.randint(0, 99)
        if (bored > 20 and config.LEARNING):
            CrownBotBrain.vocalizeNew()
        else:
            CrownBotBrain.vocalizeFromCache()
        CrownBotBrain.brain_shuffle()
        pause(random.randint(10, 60))
    else:
        CrownBotBrain.vocalizeFromCache()
        CrownBotBrain.brain_shuffle()
        pause(random.randint(10, 60))


def main():
    """Main entry point of the program."""
    setup()
    loop()


if __name__ == "__main__":
    main()
