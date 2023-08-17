from dataclasses import dataclass
from typing import Optional


@dataclass
class WorkflowContext:
    workflow_id: str
    workflow_run_id: str
    workflow_start_timestamp_seconds: int
    state_execution_id: Optional[str] = None
    first_attempt_timestamp_seconds: Optional[int] = None
    attempt: Optional[int] = None
