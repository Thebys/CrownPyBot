from enum import Enum
import random


class Locations(Enum):
    """An enumeration of locations available for use in the prompt generator."""
    THE_HOARDERS_FLAT = "The cursed hoarders flat on Zahradníkova street in Brno where I was stuck in for 30 years since 1993."
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
    KLOBASOVE_KRALOVSTVI = "Klobásové Království."
    KLOBASKOVE_KRALOVSTVI = "Klobáksové Království."
    JABLONEC_NAD_NISOU = "Jablonec nad Nisou."
    BRNO = "Brno."
    BERLIN = "Berlin."
    NUCLEAR_WASTELAND = "The nuclear wasteland."
    THE_WASTELAND = "The wasteland."
    BUNKER = "The bunker."
    PRAGUE_CASTLE = "Prague Castle."
    KAMPA_PARK = "Kampa Park."
    KARLSTEJN_CASTLE = "Karlstejn Castle."
    CHARLES_BRIDGE = "Charles Bridge."
    THE_MUSEUM = "The museum."
    THE_LIBRARY = "The library."
    THE_HOSPITAL = "The hospital."
    THE_SCHOOL = "The school."
    THE_UNIVERSITY = "The university."
    THE_COLLEGE = "The college."
    THE_CHURCH = "The church."
    
    

    def random(self):
        """Return a random location."""
        return random.choice(list(Locations))
