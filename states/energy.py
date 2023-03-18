from enum import Enum


class Energy(Enum):
    """Energy level palette of the machine."""
    EXHAUSTED = 1
    TIRED = 2
    NORMAL = 3
    ENERGIZED = 4
    HYPER = 5

    def _missing_(value):
        """Return the closest energy level for a given value when out of range."""
        if value < 1:
            return Energy.EXHAUSTED
        else:
            return Energy.HYPER

    def __str__(self):
        """Return a string representation of the energy level."""
        if self == Energy.EXHAUSTED:
            return "exhausted"
        elif self == Energy.TIRED:
            return "tired"
        elif self == Energy.NORMAL:
            return "normal"
        elif self == Energy.ENERGIZED:
            return "energized"
        else:
            return "HYPER"
