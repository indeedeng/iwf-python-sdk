from dataclasses import dataclass

from iwf_api.models import (
    WorkflowStateWaitUntilRequest,
    WorkflowStateWaitUntilResponse,
    WorkflowStateExecuteRequest,
    WorkflowStateExecuteResponse,
)

from iwf.command_request import _to_idl_command_request
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.object_encoder import ObjectEncoder
from iwf.persistence import Persistence
from iwf.registry import Registry
from iwf.state_decision import _to_idl_state_decision
from iwf.utils.iwf_typing import unset_to_none
from iwf.workflow_context import _from_idl_context

workflow_state_wait_until_api_path = "/api/v1/workflowState/start"
workflow_state_execute_api_path = "/api/v1/workflowState/decide"


@dataclass
class WorkerOptions:
    object_encoder: ObjectEncoder


default_worker_options = WorkerOptions(ObjectEncoder.default)


class WorkerService:
    def __init__(
        self, registry: Registry, options: WorkerOptions = default_worker_options
    ):
        self._registry = registry
        self._options = options

    def handle_workflow_state_wait_until(
        self,
        request: WorkflowStateWaitUntilRequest,
    ) -> WorkflowStateWaitUntilResponse:
        state = self._registry.get_workflow_state_with_check(
            request.workflow_type, request.workflow_state_id
        )

        context = _from_idl_context(request.context)
        _input = self._options.object_encoder.decode(
            unset_to_none(request.state_input), state.get_input_type()
        )
        persistence = Persistence()
        communication = Communication()
        command_request = state.wait_until(context, _input, persistence, communication)
        return WorkflowStateWaitUntilResponse(
            command_request=_to_idl_command_request(command_request)
        )

    def handle_workflow_state_execute(
        self,
        request: WorkflowStateExecuteRequest,
    ) -> WorkflowStateExecuteResponse:
        state = self._registry.get_workflow_state_with_check(
            request.workflow_type, request.workflow_state_id
        )

        context = _from_idl_context(request.context)

        _input = self._options.object_encoder.decode(
            unset_to_none(request.state_input), state.get_input_type()
        )
        persistence = Persistence()
        communication = Communication()
        command_results = CommandResults()
        decision = state.execute(
            context, _input, command_results, persistence, communication
        )
        return WorkflowStateExecuteResponse(
            state_decision=_to_idl_state_decision(
                decision,
                request.workflow_type,
                self._registry,
                self._options.object_encoder,
            )
        )
