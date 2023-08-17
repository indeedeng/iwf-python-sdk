from dataclasses import dataclass
from typing import Any, Union

from iwf.errors import WorkflowDefinitionError
from iwf.workflow_state import WorkflowState, get_state_id_by_class


@dataclass
class StateMovement:
    state_id: str
    state_input: Any = None


reserved_state_id_prefix = "_SYS_"

graceful_completing_sys_state_id = (
    reserved_state_id_prefix + "GRACEFUL_COMPLETING_WORKFLOW"
)
force_completing_sys_state_id = reserved_state_id_prefix + "FORCE_COMPLETING_WORKFLOW"
force_failing_sys_state_id = reserved_state_id_prefix + "FORCE_FAILING_WORKFLOW"
dead_end_sys_state_id = reserved_state_id_prefix + "DEAD_END"


dead_end = StateMovement(dead_end_sys_state_id)


def graceful_complete_workflow(output: Any = None) -> StateMovement:
    return StateMovement(graceful_completing_sys_state_id, output)


def force_complete_workflow(output: Any = None) -> StateMovement:
    return StateMovement(force_completing_sys_state_id, output)


def force_fail_workflow(output: Any = None) -> StateMovement:
    return StateMovement(force_failing_sys_state_id, output)


def state_movement(
    state: Union[str, type[WorkflowState]], state_input: Any = None
) -> StateMovement:
    if isinstance(state, str):
        state_id = state
    else:
        state_id = get_state_id_by_class(state)
    if state_id.startswith(reserved_state_id_prefix):
        raise WorkflowDefinitionError("cannot use reserved stateId")
    return StateMovement(state_id, state_input)
