from enum import Enum


class CommandWaitingType(str, Enum):
    ALL_COMPLETED = "ALL_COMPLETED"
    ANY_COMBINATION_COMPLETED = "ANY_COMBINATION_COMPLETED"
    ANY_COMPLETED = "ANY_COMPLETED"

    def __str__(self) -> str:
        return str(self.value)
