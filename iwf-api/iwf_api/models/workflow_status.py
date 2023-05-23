from enum import Enum


class WorkflowStatus(str, Enum):
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    CONTINUED_AS_NEW = "CONTINUED_AS_NEW"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    TERMINATED = "TERMINATED"
    TIMEOUT = "TIMEOUT"

    def __str__(self) -> str:
        return str(self.value)
