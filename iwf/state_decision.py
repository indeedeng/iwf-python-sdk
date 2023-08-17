from __future__ import annotations  # <-- Additional import.

import typing

if typing.TYPE_CHECKING:
    from iwf.registry import Registry
    from iwf.workflow_state import WorkflowState

from dataclasses import dataclass
from typing import List, Any, Union

from iwf_api.models.state_decision import StateDecision as IdlStateDecision

from iwf.object_encoder import ObjectEncoder

from iwf.state_movement import (
    StateMovement,
    dead_end_state_movement,
    graceful_complete_workflow_state_movement,
    force_complete_workflow_state_movement,
    force_fail_workflow_state_movement,
    state_movement,
    _to_idl_state_movement,
)


@dataclass
class StateDecision:
    next_states: List[StateMovement]


dead_end = StateDecision([dead_end_state_movement])


def graceful_complete_workflow(output: Any = None) -> StateDecision:
    return StateDecision([graceful_complete_workflow_state_movement(output)])


def force_complete_workflow(output: Any = None) -> StateDecision:
    return StateDecision([force_complete_workflow_state_movement(output)])


def force_fail_workflow(output: Any = None) -> StateDecision:
    return StateDecision([force_fail_workflow_state_movement(output)])


def single_next_state(
    state: Union[str, type[WorkflowState]], state_input: Any = None
) -> StateDecision:
    return StateDecision([state_movement(state, state_input)])


def multi_next_states(next_states: List[StateMovement]) -> StateDecision:
    return StateDecision(next_states)


def _to_idl_state_decision(
    decision: StateDecision, wf_type: str, registry: Registry, encoder: ObjectEncoder
) -> IdlStateDecision:
    return IdlStateDecision(
        [
            _to_idl_state_movement(movement, wf_type, registry, encoder)
            for movement in decision.next_states
        ]
    )
