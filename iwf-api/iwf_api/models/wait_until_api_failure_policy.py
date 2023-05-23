from enum import Enum


class WaitUntilApiFailurePolicy(str, Enum):
    FAIL_WORKFLOW_ON_FAILURE = "FAIL_WORKFLOW_ON_FAILURE"
    PROCEED_ON_FAILURE = "PROCEED_ON_FAILURE"

    def __str__(self) -> str:
        return str(self.value)
