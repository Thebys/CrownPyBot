from enum import Enum
import random


class Eras(Enum):
    """An enumeration of eras available for use in the prompt generator."""
    THE_PAST = "The past."
    THE_RECENT_PAST = "The recent past."
    THE_80S = "The 80s."
    YEAR_1980 = "The year 1980, the year you were manufactured."
    YEAR_1984 = "The year 1984."
    THE_90S = "The 90s."
    YEAR_1993 = "The year 1993."
    YEAR_1999 = "The year 1999."
    YEAR_2004 = "The year 2004."
    YEAR_2014 = "The year 2014."
    YEAR_2019 = "The year 2019."
    YEAR_2023 = "The year 2023."
    YEAR_2024 = "The year 2024."
    THE_PRESENT = "The present."
    THE_FUTURE = "The future."

    def random(self):
        """Return a random era."""
        return random.choice(list(Eras))
