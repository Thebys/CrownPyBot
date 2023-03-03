import logging
import random
import time
from MachineBrain import MachineBrain

def setup():
    logging.basicConfig(filename="CrownPiBot.log", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.debug("Setup started.")
    CrownBotBrain = MachineBrain()


def loop():
    while (True):
        CrownBotBrain = MachineBrain.instance
        scenario = random.randint(0, 9)
        if (scenario == 1):
            CrownBotBrain.vocalizeNew()
            time.sleep(30)
        else:
            CrownBotBrain.vocalizeFromCache()
            time.sleep(10)
        CrownBotBrain.shuffle()


def main():
    setup()
    loop()


if __name__ == "__main__":
    main()
