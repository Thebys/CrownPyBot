from enum import Enum, auto
import logging
import json


class EventTypes(Enum):
    """Event types."""
    MACHINE_STARTUP = auto()
    MACHINE_SLEEP = auto()
    MACHINE_SHUTDOWN = auto()
    MACHINE_ERROR = auto()
    MACHINE_IDLE = auto()
    MACHINE_BORED = auto()
    MACHINE_ATTENTION_SEEKING = auto()
    INPUT_PIR_DETECTED = auto()

    def __str__(self):
        """Return a string representation of the event type, usefull for prompting."""
        if self == EventTypes.MACHINE_STARTUP:
            return "The machine starts up."
        elif self == EventTypes.MACHINE_SLEEP:
            return "The machine sleeps."
        elif self == EventTypes.MACHINE_IDLE:
            return "The machine is idle."
        elif self == EventTypes.MACHINE_BORED:
            return "The machine is bored."
        elif self == EventTypes.MACHINE_ATTENTION_SEEKING:
            return "The machine is seeking attention."
        elif self == EventTypes.INPUT_PIR_DETECTED:
            return "The machine detects motion."
        else:
            return "Unknown."


class Event:
    def __init__(self, event_type, data=None):
        self.type = event_type
        self.data = data


class EventQueue:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        logging.debug(f"EQ - Adding: {event.type} - {event.data}.")
        self.events.append(event)

    def get_events(self):
        return self.events

    def clear_events(self):
        self.events = []

    def get_event_to_handle(self):
        if len(self.events) > 0:
            logging.debug(
                f"EQ - Handling: {self.events[0].type.name} Data: {self.events[0].data}.")
            return self.events.pop(0)
        return None

    def get_event_of_type(self, event_type):
        for event in self.events:
            if event.type == event_type:
                return event
        return None

    def remove_event(self, event_type):
        for event in self.events:
            if event.type == event_type:
                self.events.remove(event)

    def empty(self):
        return len(self.events) == 0

    def has_event(self, event_type):
        for event in self.events:
            if event.type == event_type:
                return True
        return False