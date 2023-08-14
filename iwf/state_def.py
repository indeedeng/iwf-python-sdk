from dataclasses import dataclass

from workflow_state import WorkflowState


@dataclass
class StateDef:
    state: WorkflowState
    can_start_workflow: bool


def starting_state(state: WorkflowState) -> StateDef:
    return StateDef(state, True)


def non_starting_state(state: WorkflowState) -> StateDef:
    return StateDef(state, False)
