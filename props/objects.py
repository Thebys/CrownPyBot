from enum import Enum
import random

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