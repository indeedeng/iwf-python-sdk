from enum import Enum


class WorkflowStopType(str, Enum):
    CANCEL = "CANCEL"
    FAIL = "FAIL"
    TERMINATE = "TERMINATE"

    def __str__(self) -> str:
        return str(self.value)
