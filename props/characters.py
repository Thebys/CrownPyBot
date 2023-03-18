from enum import Enum


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
