from enum import Enum


class ChannelRequestStatus(str, Enum):
    RECEIVED = "RECEIVED"
    WAITING = "WAITING"

    def __str__(self) -> str:
        return str(self.value)
