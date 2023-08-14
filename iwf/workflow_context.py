from dataclasses import dataclass


@dataclass
class WorkflowContext:
    workflow_id: str
    workflow_run_id: str
    state_execution_id: str
    workflow_start_timestamp_seconds: int
    first_attempt_timestamp_seconds: int
    attempt: int
