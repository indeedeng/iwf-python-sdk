from dataclasses import dataclass
from typing import Optional

from iwf.iwf_api.models.context import Context
from iwf.utils.iwf_typing import unset_to_none


@dataclass
class WorkflowContext:
    workflow_id: str
    workflow_run_id: str
    workflow_start_timestamp_seconds: int
    state_execution_id: Optional[str] = None
    first_attempt_timestamp_seconds: Optional[int] = None
    attempt: Optional[int] = None
    child_workflow_request_id: Optional[str] = None


def _from_idl_context(idl_context: Context) -> WorkflowContext:
    state_execution_id = unset_to_none(idl_context.state_execution_id)

    return WorkflowContext(
        workflow_id=idl_context.workflow_id,
        workflow_run_id=idl_context.workflow_run_id,
        workflow_start_timestamp_seconds=idl_context.workflow_started_timestamp,
        state_execution_id=state_execution_id,
        first_attempt_timestamp_seconds=unset_to_none(
            idl_context.first_attempt_timestamp,
        ),
        attempt=unset_to_none(idl_context.attempt),
        child_workflow_request_id=(
            idl_context.workflow_run_id + "-" + state_execution_id
            if state_execution_id is not None
            else None
        ),
    )
