from enum import Enum

class AlphabetOption(Enum):
    FORWARD = "Move forward"
    LEFT = "Turn left"
    RIGHT = "Turn right"
    PUSH = "Push"
    POP = "Pop"
    STOP = "Stop"