import logging
import random
import time
import config
import MachineBrain
from MachineBrain import Set
from MachineBrain import MachineBrain
from events import EventQueue, EventTypes, Event


def setup():
    """Setup the machine."""
    logging.basicConfig(filename="CrownPiBot.log", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.debug("Setup started.")
    MachineBrain()


def loop():
    """Loop the machine's life."""
    while (True):
        process_queue()
        time.sleep(0.1)  # Safety net to prevent CPU hogging


def process_queue():
    """Process the machine's event queue."""
    CrownBotBrain = MachineBrain.instance
    while not CrownBotBrain.event_queue.empty():
        event = CrownBotBrain.event_queue.get_event_to_handle()
        if event is not None:
            handle_event(event)
    # If the queue is empty, add an idle event to prevent the machine from freezing.
    CrownBotBrain.event_queue.add_event(Event(EventTypes.MACHINE_IDLE))


def handle_event(event):
    """Handle an event."""
    type = event.type
    CrownBotBrain = MachineBrain.instance
    if type == EventTypes.MACHINE_STARTUP:
        CrownBotBrain.startup()
    elif type == EventTypes.MACHINE_SLEEP:
        CrownBotBrain.sleep(event.data)
    elif type == EventTypes.DIRECT_SPEECH:
        CrownBotBrain.vocalize_direct(event.data, event)
    elif type == EventTypes.SAY_TIME:
        CrownBotBrain.vocalize_current_time(event)
    elif type == EventTypes.SAY_RANDOM_MEMORY:
        CrownBotBrain.vocalize_random_memory(event)
    elif type == EventTypes.SAY_PRAISE_VAULT_TEC:
        CrownBotBrain.vocalize_praise_vault_tec(event)
    elif type == EventTypes.MACHINE_IDLE:
        if (config.LEARNING):
            choice = random.randint(0, 3)
            if (choice == 0):
                CrownBotBrain.event_queue.add_event(
                    Event(EventTypes.SAY_RANDOM_MEMORY))
            elif (choice == 1):
                CrownBotBrain.event_queue.add_event(Event(EventTypes.SAY_TIME))
            elif (choice == 2):
                CrownBotBrain.vocalize_from_cache()
            elif (choice == 3):
                CrownBotBrain.event_queue.add_event(
                    Event(EventTypes.SAY_PRAISE_VAULT_TEC))
            CrownBotBrain.event_queue.add_event(
                Event(EventTypes.MACHINE_SLEEP, random.randint(10, 30)))

        else:
            CrownBotBrain.vocalize_from_cache()
        CrownBotBrain.event_queue.add_event(
            Event(EventTypes.MACHINE_SLEEP, random.randint(10, 30)))
    else:
        logging.debug(f"Unknown event: {event}")


def main():
    """Main entry point of the program."""
    setup()
    loop()


if __name__ == "__main__":
    main()
