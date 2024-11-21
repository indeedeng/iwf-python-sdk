from __future__ import annotations  # <-- Additional import.

import typing

from iwf_api.models import WorkflowConditionalClose, WorkflowConditionalCloseType

from iwf.errors import WorkflowDefinitionError

if typing.TYPE_CHECKING:
    from iwf.registry import Registry
    from iwf.workflow_state import WorkflowState

from dataclasses import dataclass
from typing import Any, List, Union

from iwf.iwf_api.models.state_decision import StateDecision as IdlStateDecision

from iwf.object_encoder import ObjectEncoder

from iwf.state_movement import StateMovement, _to_idl_state_movement


@dataclass
class InternalConditionalClose:
    conditional_close_type: WorkflowConditionalCloseType

    channel_name: str

    close_input: Any = None


@dataclass
class StateDecision:
    next_states: List[StateMovement]

    conditional_close: typing.Optional[InternalConditionalClose] = None

    dead_end: typing.ClassVar[StateDecision]

    @classmethod
    def graceful_complete_workflow(cls, output: Any = None) -> StateDecision:
        return StateDecision([StateMovement.graceful_complete_workflow(output)])

    @classmethod
    def force_complete_workflow(cls, output: Any = None) -> StateDecision:
        return StateDecision([StateMovement.force_complete_workflow(output)])

    @classmethod
    def force_fail_workflow(cls, output: Any = None) -> StateDecision:
        return StateDecision([StateMovement.force_fail_workflow(output)])

    @classmethod
    def single_next_state(
        cls, state: Union[str, type[WorkflowState]], state_input: Any = None
    ) -> StateDecision:
        return StateDecision([StateMovement.create(state, state_input)])

    @classmethod
    def multi_next_states(
        cls, *next_states: Union[type[WorkflowState], StateMovement]
    ) -> StateDecision:
        next_list = [
            n if isinstance(n, StateMovement) else StateMovement.create(n)
            for n in next_states
        ]
        return StateDecision(next_list)

    # Atomically force complete the workflow if internal channel is empty, otherwise trigger the state movements from the current thread
    # This is to ensure all the messages in the channel are processed before completing the workflow, otherwise messages may be lost.
    # Without this atomic API, if just checking the channel emptiness in the State WaitUntil, a workflow may receive new messages during the
    # execution of state APIs.
    #
    # Note that it's only for internal messages published from RPCs.
    # It doesn't cover the cases that internal messages are published from other State APIs.
    # If you do want to use other State APIs to publish messages to the channel at the same time, you can use persistence locking to
    # ensure only the State APIs are not executed in parallel.
    @classmethod
    def force_complete_if_internal_channel_empty_or_else(
        cls, internal_channel_name: str, output: Any = None
    ) -> StateDecision:
        return StateDecision(
            [],
            InternalConditionalClose(
                WorkflowConditionalCloseType.FORCE_COMPLETE_ON_INTERNAL_CHANNEL_EMPTY,
                internal_channel_name,
                output,
            ),
        )

    # Atomically force complete the workflow if signal channel is empty, otherwise trigger the state movements from the current thread
    # This is to ensure all the messages in the channel are processed before completing the workflow, otherwise messages may be lost.
    # Without this atomic API, if just checking the channel emptiness in the State WaitUntil, a workflow may receive new messages during the
    # execution of state APIs.
    @classmethod
    def force_complete_if_signal_channel_empty_or_else(
        cls, signal_channel_name: str, output: Any = None
    ) -> StateDecision:
        return StateDecision(
            [],
            InternalConditionalClose(
                WorkflowConditionalCloseType.FORCE_COMPLETE_ON_SIGNAL_CHANNEL_EMPTY,
                signal_channel_name,
                output,
            ),
        )


StateDecision.dead_end = StateDecision([StateMovement.dead_end])


def _to_idl_state_decision(
    decision: StateDecision, wf_type: str, registry: Registry, encoder: ObjectEncoder
) -> IdlStateDecision:
    if len(decision.next_states) > 0:
        return IdlStateDecision(
            [
                _to_idl_state_movement(movement, wf_type, registry, encoder)
                for movement in decision.next_states
            ]
        )
    else:
        internal_conditional_close = decision.conditional_close
        if internal_conditional_close is None:
            raise WorkflowDefinitionError(
                "must have either next states or conditional close"
            )

        conditional_close = WorkflowConditionalClose(
            conditional_close_type=internal_conditional_close.conditional_close_type,
            channel_name=internal_conditional_close.channel_name,
            close_input=encoder.encode(internal_conditional_close.close_input),
        )
        return IdlStateDecision([], conditional_close)
