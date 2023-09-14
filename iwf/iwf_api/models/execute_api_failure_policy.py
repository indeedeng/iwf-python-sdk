from enum import Enum


class ExecuteApiFailurePolicy(str, Enum):
    FAIL_WORKFLOW_ON_EXECUTE_API_FAILURE = "FAIL_WORKFLOW_ON_EXECUTE_API_FAILURE"
    PROCEED_TO_CONFIGURED_STATE = "PROCEED_TO_CONFIGURED_STATE"

    def __str__(self) -> str:
        return str(self.value)
