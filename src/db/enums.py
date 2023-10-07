from enum import Enum, IntEnum


class HeadacheIntensity(IntEnum):
    WEAK = 1
    MEDIUM = 2
    STRONG = 3


class HeadacheSide(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


class RemedyResult(str, Enum):
    NO_EFFECT = '-'
    SLOW_EFFECT = '+'
    FAST_EFFECT = '++'
