from enum import StrEnum

class AlphabetOption(StrEnum):
    FORWARD = "Move forward"
    LEFT = "Turn left"
    RIGHT = "Turn right"
    PUSH = "Push"
    POP = "Pop"
    STOP = "Stop"