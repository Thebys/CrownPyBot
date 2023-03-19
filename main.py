import logging
import time
import config
import multiprocessing
import MachineBrain
from TelegramBot import CrownTelegramBot
from MachineBrain import MachineBrain
from events import EventQueue, EventTypes, Event


def main():
    """Main entry point of the program. Imagine setup() and loop() in Arduino."""
    if (config.DEVELOPMENT):
        logging.basicConfig(filename="CrownPiBot.log", level=logging.DEBUG)
        logging.getLogger().addHandler(logging.StreamHandler())
    logging.debug("PC - Setup started.")

    # Create Crown <> TG communication queue
    queue = multiprocessing.Queue()

    crown_brain = MachineBrain(queue)
    telegram_bot = CrownTelegramBot()
    telegram_bot.init_telegram_bot(queue)
    logging.debug("PC - Setup finished.")
    loop(crown_brain, telegram_bot, queue)


def loop(CrownBrain, TelegramBot, CrownTelegramQueue):
    """Loop the machine's life."""
    while (True):
        # Check if the Telegram bot is still running.
        if (TelegramBot.enabled):
            TelegramBot.check_telegram_bot()
        
        # Check if there are any events in the CrownTelegramQueue
        while not CrownTelegramQueue.empty():
            event = CrownTelegramQueue.get()
            CrownBrain.event_queue.add_event(event)
        
        # Handle events from the queue.
        while not CrownBrain.event_queue.empty():
            event = CrownBrain.event_queue.get_event_to_handle()
            if event is not None:
                CrownBrain.handle_event(event)
        # Advance the machine's state, maybew could be moved.
        CrownBrain.advance()
        time.sleep(1)
        # If the queue is empty, add an idle event to prevent the machine from freezing.
        CrownBrain.event_queue.add_event(Event(EventTypes.MACHINE_IDLE))


 # Actually run the program...
if __name__ == "__main__":
    main()
