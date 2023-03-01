import logging

from MachineBrain import MachineBrain


def setup():
    logging.basicConfig(filename="CrownPiBot.log", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.debug("Setup started.")
    CrownBotBrain = MachineBrain()


def loop():
    while (True):
        CrownBotBrain = MachineBrain.instance
        CrownBotBrain.vocalize()


def main():
    setup()
    loop()


if __name__ == "__main__":
    main()
