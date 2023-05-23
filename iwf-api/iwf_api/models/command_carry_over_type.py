from enum import Enum


class CommandCarryOverType(str, Enum):
    NONE = "NONE"

    def __str__(self) -> str:
        return str(self.value)
