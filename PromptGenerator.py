from enum import Enum
import random
import logging

# This file contains several scene enumartion classes and a class that assits in prompt construction.


class Era(Enum):
    """An enumeration of eras available for use in the prompt generator."""
    THE_PAST = "The past."
    THE_80S = "The 80s."
    YEAR_1980 = "The year 1980. I was made then."
    YEAR_1984 = "The year 1984."
    THE_90S = "The 90s."
    YEAR_1993 = "The year 1993."
    YEAR_1999 = "The year 1999."
    YEAR_2004 = "The year 2004."
    YEAR_2014 = "The year 2014."
    YEAR_2019 = "The year 2019."
    YEAR_2023 = "The year 2023."
    THE_PRESENT = "The present."
    THE_FUTURE = "The future."


class Location(Enum):
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


class Characters(Enum):
    """"An enumeration of characters available for use in the prompt generator."""
    MYSTERIOUS_HACKER = "mysterious hacker"
    MYSTERIOUS_STRANGER = "mysterious stranger"
    RECEPTIONIST = "receptionist"
    BARTENDER = "bartender"
    WAITER = "waiter"
    WAITRESS = "waitress"
    CASINO_DEALER = "casino dealer"
    CASINO_MANAGER = "casino manager"
    MANAGER = "manager"
    COOK = "cook"
    CHEF = "chef"
    EMPLOYEE = "employee"
    ELEVATOR_SERVICEMAN = "elevator serviceman"
    MUSIC_BAND_MEMBER = "music band member"
    MUSIC_BAND_LEADER = "music band leader"
    MUSIC_PRODUCER = "music producer"
    DRUG_DEALER = "drug dealer"
    DRUG_ADDICT = "drug addict"
    DRIVER = "driver"
    TAXI_DRIVER = "taxi driver"
    POLICE_OFFICER = "police officer"
    FIREFIGHTER = "firefighter"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"
    FAMILY_MEMBER = "family member"
    FAMILY = "family"

    def __str__(self) -> str:
        return self.value

    def random():
        """Return a random character."""
        return random.choice(list(Characters))


class Objects(Enum):
    """An enumeration of objects available for use in the prompt generator."""
    CAR = "car"
    TRUCK = "truck"
    VAN = "van"
    MOTORCYCLE = "motorcycle"
    BIKE = "bike"
    SCOOTER = "scooter"
    ELECTRIC_SCOOTER = "electric scooter"
    ELECTRIC_BIKE = "electric bike"
    ELECTRIC_CAR = "electric car"
    SMARTPHONE = "smartphone"
    LAPTOP = "laptop"
    CASH_REGISTER = "cash register"
    ELEVATOR = "elevator"
    STAIRS = "stairs"
    MONEY = "money"
    CASH = "cash"
    CREDIT_CARD = "credit card"
    VIOLIN = "violin"
    GUITAR = "guitar"
    PIANO = "piano"
    GUN = "gun"
    BOOK = "book"
    MAGAZINE = "magazine"
    LETTER = "letter"
    NOTE = "note"
    PROTEIN_BAR = "protein bar"
    JOINT = "joint"
    BEER = "beer"
    BOTTLE = "bottle"
    CAN_OF_NUKA_COLA = "can of Nuka Cola"
    VENDING_MACHINE = "vending machine"
    COFFEE_MACHINE = "coffee machine"
    COFFEE = "coffee"
    PIZZA = "pizza"
    BURGER = "burger"
    PHONE = "phone"
    PHONE_CALL = "phone call"
    NEWSPAPER = "newspaper"
    TV = "TV"
    RADIO = "radio"

    def __str__(self) -> str:
        return self.value

    def random():
        """Return a random object."""
        return random.choice(list(Objects))


class PromptGenerator:
    """A class that assists in prompt construction."""

    def __init__(self):
        """Initialize the prompt generator so far with random properties."""
        self.characters = dict()
        self.objects = dict()
        self.set_random_properties()

    def set_random_properties(self):
        """Set random generator properties to single era and location and possible multiple characters and objects."""
        self.era = Era(random.choice(list(Era)))
        self.location = Location(random.choice(list(Location)))
        number_of_characters = random.randint(1, 3)
        for _ in range(number_of_characters):
            self.characters[_] = Characters.random()
        number_of_objects = random.randint(1, 3)
        for _ in range(number_of_objects):
            self.objects[_] = Objects.random()

    def generate_random_memory_prompt(self, emotion = ""):
        """Generate a memory prompt."""
        # Convert character and object lists to comma-separated strings
        characters = ', '.join(str(ch) for ch in self.characters.values())
        objects = ', '.join(str(ob) for ob in self.objects.values())

        prompt = f"You tell a short {emotion} memory anecdote. Location? { self.location.value } Time? {self.era.value} It is about {characters} and {objects}."
        return prompt

    def praise_vault_tec(self):
        """Generate a prompt praising Vault-Tec."""
        prompt = f"You greet passer-bys with an over the top post apocalyptic irony punchline for the Vaultek."
        return prompt
