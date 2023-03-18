from enum import Enum


class Stress(Enum):
    """Stress level palette of the machine."""
    CALM = 1
    NEUTRAL = 2
    NERVOUS = 3
    TENSE = 4
    STRESSED = 5
    RAGING = 6

    def _missing_(value):
        """Return the closest stress level for a given value when out of range."""
        if value < 1:
            return Stress.CALM
        elif value > 6:
            return Stress.RAGING
        else:
            return Stress(value)

    def __str__(self):
        """Return a string representation of the stress level."""
        if self == Stress.CALM:
            return "calm"
        elif self == Stress.NEUTRAL:
            return "neutral"
        elif self == Stress.NERVOUS:
            return "nervous"
        elif self == Stress.TENSE:
            return "tense"
        elif self == Stress.STRESSED:
            return "stressed"
        else:
            return "raging"
