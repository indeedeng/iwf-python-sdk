from dataclasses import dataclass, field
from typing import List

from workflow_state import WorkflowState


@dataclass
class StateDef:
    state: WorkflowState
    can_start_workflow: bool


def starting_state(state: WorkflowState) -> StateDef:
    return StateDef(state, True)


def non_starting_state(state: WorkflowState) -> StateDef:
    return StateDef(state, False)


@dataclass
class StateSchema:
    states: List[StateDef] = field(default_factory=list)
