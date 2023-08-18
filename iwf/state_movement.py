from __future__ import annotations

import typing
from typing import Union

from iwf.errors import WorkflowDefinitionError

if typing.TYPE_CHECKING:
    from iwf.workflow_state import (
        WorkflowState,
    )
    from iwf.registry import Registry

from dataclasses import dataclass
from typing import Any

from iwf_api.models.state_movement import StateMovement as IdlStateMovement

from iwf.object_encoder import ObjectEncoder

from iwf.workflow_state_options import _to_idl_state_options


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


dead_end_state_movement = StateMovement(dead_end_sys_state_id)


def graceful_complete_workflow_state_movement(output: Any = None) -> StateMovement:
    return StateMovement(graceful_completing_sys_state_id, output)


def force_complete_workflow_state_movement(output: Any = None) -> StateMovement:
    return StateMovement(force_completing_sys_state_id, output)


def force_fail_workflow_state_movement(output: Any = None) -> StateMovement:
    return StateMovement(force_failing_sys_state_id, output)


def state_movement(
    state: Union[str, type[WorkflowState]], state_input: Any = None
) -> StateMovement:
    if isinstance(state, str):
        state_id = state
    else:
        from iwf.workflow_state import (
            get_state_id_by_class,
        )

        state_id = get_state_id_by_class(state)
    if state_id.startswith(reserved_state_id_prefix):
        raise WorkflowDefinitionError("cannot use reserved stateId")
    return StateMovement(state_id, state_input)


def _to_idl_state_movement(
    movement: StateMovement, wf_type: str, registry: Registry, encoder: ObjectEncoder
) -> IdlStateMovement:
    idl_movement = IdlStateMovement(
        state_id=movement.state_id, state_input=encoder.encode(movement.state_input)
    )
    if not movement.state_id.startswith(reserved_state_id_prefix):
        state = registry.get_workflow_state_with_check(wf_type, movement.state_id)
        idl_state_options = _to_idl_state_options(state.get_state_options())
        from iwf.workflow_state import (
            should_skip_wait_until,
        )

        if should_skip_wait_until(state):
            idl_state_options.skip_wait_until = True
        idl_movement.state_options = idl_state_options
    return idl_movement
