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
    _to_idl_state_movement,
)


@dataclass
class StateDecision:
    next_states: List[StateMovement]


dead_end = StateDecision([StateMovement.dead_end])


def graceful_complete_workflow(output: Any = None) -> StateDecision:
    return StateDecision([StateMovement.graceful_complete_workflow(output)])


def force_complete_workflow(output: Any = None) -> StateDecision:
    return StateDecision([StateMovement.force_complete_workflow(output)])


def force_fail_workflow(output: Any = None) -> StateDecision:
    return StateDecision([StateMovement.force_fail_workflow(output)])


def single_next_state(
    state: Union[str, type[WorkflowState]], state_input: Any = None
) -> StateDecision:
    return StateDecision([StateMovement.create(state, state_input)])


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
