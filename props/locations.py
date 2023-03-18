from enum import Enum
import random

class Locations(Enum):
    """An enumeration of locations available for use in the prompt generator."""
    THE_HOARDERS_FLAT = "The cursed hoarders flat I was stuck in for 30 years since 1993."
    THE_GARAGE = "The garage."
    THE_BACKYARD = "The backyard."
    THE_STORE = "The store."
    THE_STREET = "The street."
    THE_PARK = "The public park."
    THE_OFFICE = "The central office."
    SCHNEIDERS_PUB = "The Schneider's pub."
    THE_RESTAURANT = "The Nowak restaurant."
    BECKERS_RESTAURANT = "Becker's restaurant."
    THE_CASINO = "The Goldbach casino."
    WIENER_WORLD = "The famous Wiener World."
    BRNO = "Brno."

    def random(self):
        """Return a random location."""
        return random.choice(list(Locations))