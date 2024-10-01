from enum import Enum


class IDReusePolicy(str, Enum):
    ALLOW_IF_NO_RUNNING = "ALLOW_IF_NO_RUNNING"
    ALLOW_IF_PREVIOUS_EXITS_ABNORMALLY = "ALLOW_IF_PREVIOUS_EXITS_ABNORMALLY"
    ALLOW_TERMINATE_IF_RUNNING = "ALLOW_TERMINATE_IF_RUNNING"
    DISALLOW_REUSE = "DISALLOW_REUSE"

    def __str__(self) -> str:
        return str(self.value)
