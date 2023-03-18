from enum import Enum


class Behavior(Enum):
    """Available behavior modes the machine can run in."""
    CALM = "calm"       # Mood apriori stable
    NORMAL = "normal"   # Mood shifts slowly
    CRAZY = "crazy"     # Mood shifts quickly and randomly
