from enum import Enum


class TimerStatus(str, Enum):
    FIRED = "FIRED"
    SCHEDULED = "SCHEDULED"

    def __str__(self) -> str:
        return str(self.value)
