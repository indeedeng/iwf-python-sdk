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

from iwf.iwf_api.iwf_api.models.state_movement import StateMovement as IdlStateMovement

from iwf.object_encoder import ObjectEncoder

from iwf.workflow_state_options import _to_idl_state_options


reserved_state_id_prefix = "_SYS_"

graceful_completing_sys_state_id = (
    reserved_state_id_prefix + "GRACEFUL_COMPLETING_WORKFLOW"
)
force_completing_sys_state_id = reserved_state_id_prefix + "FORCE_COMPLETING_WORKFLOW"
force_failing_sys_state_id = reserved_state_id_prefix + "FORCE_FAILING_WORKFLOW"
dead_end_sys_state_id = reserved_state_id_prefix + "DEAD_END"


@dataclass
class StateMovement:
    state_id: str
    state_input: Any = None

    dead_end: typing.ClassVar[StateMovement]

    @classmethod
    def graceful_complete_workflow(cls, output: Any = None) -> StateMovement:
        return StateMovement(graceful_completing_sys_state_id, output)

    @classmethod
    def force_complete_workflow(cls, output: Any = None) -> StateMovement:
        return StateMovement(force_completing_sys_state_id, output)

    @classmethod
    def force_fail_workflow(cls, output: Any = None) -> StateMovement:
        return StateMovement(force_failing_sys_state_id, output)

    @classmethod
    def create(
        cls, state: Union[str, type[WorkflowState]], state_input: Any = None
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


StateMovement.dead_end = StateMovement(dead_end_sys_state_id)


def _to_idl_state_movement(
    movement: StateMovement, wf_type: str, registry: Registry, encoder: ObjectEncoder
) -> IdlStateMovement:
    idl_movement = IdlStateMovement(
        state_id=movement.state_id, state_input=encoder.encode(movement.state_input)
    )
    if not movement.state_id.startswith(reserved_state_id_prefix):
        state = registry.get_workflow_state_with_check(wf_type, movement.state_id)

        from iwf.workflow_state import (
            should_skip_wait_until,
        )

        idl_state_options = _to_idl_state_options(
            should_skip_wait_until(state),
            state.get_state_options(),
            registry.get_state_store(wf_type),
        )

        idl_movement.state_options = idl_state_options
    return idl_movement
