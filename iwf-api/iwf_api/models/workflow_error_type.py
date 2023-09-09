from enum import Enum


class WorkflowErrorType(str, Enum):
    CLIENT_API_FAILING_WORKFLOW_ERROR_TYPE = "CLIENT_API_FAILING_WORKFLOW_ERROR_TYPE"
    INVALID_USER_WORKFLOW_CODE_ERROR_TYPE = "INVALID_USER_WORKFLOW_CODE_ERROR_TYPE"
    RPC_ACQUIRE_LOCK_FAILURE = "RPC_ACQUIRE_LOCK_FAILURE"
    SERVER_INTERNAL_ERROR_TYPE = "SERVER_INTERNAL_ERROR_TYPE"
    STATE_API_FAIL_MAX_OUT_RETRY_ERROR_TYPE = "STATE_API_FAIL_MAX_OUT_RETRY_ERROR_TYPE"
    STATE_DECISION_FAILING_WORKFLOW_ERROR_TYPE = "STATE_DECISION_FAILING_WORKFLOW_ERROR_TYPE"

    def __str__(self) -> str:
        return str(self.value)
