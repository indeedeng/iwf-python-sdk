from enum import Enum


class WorkflowConfigExecutingStateIdMode(str, Enum):
    DISABLED = "DISABLED"
    ENABLED_FOR_ALL = "ENABLED_FOR_ALL"
    ENABLED_FOR_STATES_WITH_WAIT_UNTIL = "ENABLED_FOR_STATES_WITH_WAIT_UNTIL"

    def __str__(self) -> str:
        return str(self.value)
