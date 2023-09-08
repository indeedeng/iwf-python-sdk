import typing
from dataclasses import dataclass

from iwf_api.models import (
    EncodedObject,
    KeyValue,
    WorkflowStateExecuteRequest,
    WorkflowStateExecuteResponse,
    WorkflowStateWaitUntilRequest,
    WorkflowStateWaitUntilResponse,
)
from iwf_api.types import Unset

from iwf.command_request import _to_idl_command_request
from iwf.command_results import from_idl_command_results
from iwf.communication import Communication
from iwf.object_encoder import ObjectEncoder
from iwf.persistence import Persistence
from iwf.registry import Registry
from iwf.state_decision import _to_idl_state_decision
from iwf.utils.iwf_typing import assert_not_unset, unset_to_none
from iwf.workflow_context import _from_idl_context
from iwf.workflow_state import get_input_type


@dataclass
class WorkerOptions:
    object_encoder: ObjectEncoder


default_worker_options = WorkerOptions(ObjectEncoder.default)


class WorkerService:
    api_path_workflow_state_wait_until: typing.ClassVar[
        str
    ] = "/api/v1/workflowState/start"
    api_path_workflow_state_execute: typing.ClassVar[
        str
    ] = "/api/v1/workflowState/decide"

    def __init__(
        self, registry: Registry, options: WorkerOptions = default_worker_options
    ):
        self._registry = registry
        self._options = options

    def handle_workflow_state_wait_until(
        self,
        request: WorkflowStateWaitUntilRequest,
    ) -> WorkflowStateWaitUntilResponse:
        wf_type = request.workflow_type
        state = self._registry.get_workflow_state_with_check(
            wf_type, request.workflow_state_id
        )
        internal_channel_types = self._registry.get_internal_channel_types(wf_type)
        data_attributes_types = self._registry.get_data_attribute_types(wf_type)

        context = _from_idl_context(request.context)
        _input = self._options.object_encoder.decode(
            unset_to_none(request.state_input), get_input_type(state)
        )

        current_data_attributes: dict[str, typing.Union[EncodedObject, None]] = {}
        if not isinstance(request.data_objects, Unset):
            current_data_attributes = {
                assert_not_unset(attr.key): unset_to_none(attr.value)
                for attr in request.data_objects
            }

        persistence = Persistence(
            data_attributes_types, self._options.object_encoder, current_data_attributes
        )
        communication = Communication(
            internal_channel_types, self._options.object_encoder
        )
        command_request = state.wait_until(context, _input, persistence, communication)

        pubs = communication.get_to_publishing_internal_channel()
        return WorkflowStateWaitUntilResponse(
            command_request=_to_idl_command_request(command_request),
            publish_to_inter_state_channel=pubs,
            upsert_data_objects=[
                KeyValue(k, v)
                for (k, v) in persistence.get_updated_values_to_return().items()
            ],
        )

    def handle_workflow_state_execute(
        self,
        request: WorkflowStateExecuteRequest,
    ) -> WorkflowStateExecuteResponse:
        wf_type = request.workflow_type
        state = self._registry.get_workflow_state_with_check(
            wf_type, request.workflow_state_id
        )
        internal_channel_types = self._registry.get_internal_channel_types(wf_type)
        data_attributes_types = self._registry.get_data_attribute_types(wf_type)
        context = _from_idl_context(request.context)

        _input = self._options.object_encoder.decode(
            unset_to_none(request.state_input), get_input_type(state)
        )

        current_data_attributes: dict[str, typing.Union[EncodedObject, None]] = {}
        if not isinstance(request.data_objects, Unset):
            current_data_attributes = {
                assert_not_unset(attr.key): unset_to_none(attr.value)
                for attr in request.data_objects
            }

        persistence = Persistence(
            data_attributes_types, self._options.object_encoder, current_data_attributes
        )
        communication = Communication(
            internal_channel_types, self._options.object_encoder
        )

        command_results = from_idl_command_results(
            request.command_results,
            internal_channel_types,
            self._options.object_encoder,
        )
        decision = state.execute(
            context, _input, command_results, persistence, communication
        )

        pubs = communication.get_to_publishing_internal_channel()
        return WorkflowStateExecuteResponse(
            state_decision=_to_idl_state_decision(
                decision,
                wf_type,
                self._registry,
                self._options.object_encoder,
            ),
            publish_to_inter_state_channel=pubs,
            upsert_data_objects=[
                KeyValue(k, v)
                for (k, v) in persistence.get_updated_values_to_return().items()
            ],
        )
