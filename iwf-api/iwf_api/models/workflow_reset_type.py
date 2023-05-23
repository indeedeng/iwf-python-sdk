from enum import Enum


class WorkflowResetType(str, Enum):
    BEGINNING = "BEGINNING"
    HISTORY_EVENT_ID = "HISTORY_EVENT_ID"
    HISTORY_EVENT_TIME = "HISTORY_EVENT_TIME"
    STATE_EXECUTION_ID = "STATE_EXECUTION_ID"
    STATE_ID = "STATE_ID"

    def __str__(self) -> str:
        return str(self.value)
