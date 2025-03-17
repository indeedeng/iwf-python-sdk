import traceback
import typing
from dataclasses import dataclass
from typing import Union

from iwf.command_request import _to_idl_command_request
from iwf.command_results import from_idl_command_results
from iwf.communication import Communication
from iwf.data_attributes import DataAttributes
from iwf.iwf_api.models import (
    EncodedObject,
    KeyValue,
    SearchAttribute,
    SearchAttributeValueType,
    WorkflowStateExecuteRequest,
    WorkflowStateExecuteResponse,
    WorkflowStateWaitUntilRequest,
    WorkflowStateWaitUntilResponse,
    WorkflowWorkerRpcRequest,
    WorkflowWorkerRpcResponse,
)
from iwf.iwf_api.types import Unset
from iwf.object_encoder import ObjectEncoder
from iwf.persistence import Persistence
from iwf.registry import Registry
from iwf.search_attributes import SearchAttributes
from iwf.state_decision import StateDecision, _to_idl_state_decision
from iwf.utils.iwf_typing import assert_not_unset, unset_to_none
from iwf.workflow_context import WorkflowContext, _from_idl_context
from iwf.workflow_state import get_input_type


@dataclass
class WorkerOptions:
    object_encoder: ObjectEncoder


default_worker_options = WorkerOptions(ObjectEncoder.default)


class WorkerService:
    api_path_workflow_state_wait_until: typing.ClassVar[str] = (
        "/api/v1/workflowState/start"
    )
    api_path_workflow_state_execute: typing.ClassVar[str] = (
        "/api/v1/workflowState/decide"
    )
    api_path_workflow_worker_rpc: typing.ClassVar[str] = "/api/v1/workflowWorker/rpc"

    def __init__(
        self, registry: Registry, options: WorkerOptions = default_worker_options
    ):
        self._registry = registry
        self._options = options

    @staticmethod
    def handle_worker_error(exception: Exception):
        """
        Handle the exception/error of worker so that Temporal/Cadence WebUI can show the error nicely.
        Example usage (in Flask):
            @_flask_app.errorhandler(Exception)
            def internal_error(exception):
                return _worker_service.handle_worker_error(exception), 500
        """
        stacktrace = traceback.format_exc()
        index = stacktrace.index("iwf-python-sdk/iwf/worker_service.py")
        return "WorkerExecutionError: {0}; StackTrace:{1}".format(
            exception, stacktrace[index:]
        )

    def handle_workflow_worker_rpc(
        self,
        request: WorkflowWorkerRpcRequest,
    ) -> WorkflowWorkerRpcResponse:
        wf_type = request.workflow_type
        rpc_info = self._registry.get_rpc_infos(wf_type)[request.rpc_name]

        internal_channel_types = self._registry.get_internal_channel_type_store(wf_type)
        signal_channel_types = self._registry.get_signal_channel_types(wf_type)
        data_attributes_types = self._registry.get_data_attribute_types(wf_type)

        context = _from_idl_context(request.context)
        _input = self._options.object_encoder.decode(
            unset_to_none(request.input_), rpc_info.input_type
        )

        current_data_attributes: dict[str, typing.Union[EncodedObject, None]] = {}
        if not isinstance(request.data_attributes, Unset):
            current_data_attributes = {
                assert_not_unset(attr.key): unset_to_none(attr.value)
                for attr in request.data_attributes
            }

        data_attributes = DataAttributes(
            data_attributes_types, self._options.object_encoder, current_data_attributes
        )

        search_attributes_types = self._registry.get_search_attribute_types(wf_type)
        search_attributes = SearchAttributes(
            search_attributes_types, unset_to_none(request.search_attributes)
        )

        persistence = Persistence(data_attributes, search_attributes)

        communication = Communication(
            internal_channel_types,
            signal_channel_types,
            self._options.object_encoder,
            unset_to_none(request.internal_channel_infos),
            unset_to_none(request.signal_channel_infos),
        )
        params: typing.Any = []
        if rpc_info.params_order is not None:
            for param_type in rpc_info.params_order:
                if param_type == Persistence:
                    params.append(persistence)
                elif param_type == Communication:
                    params.append(communication)
                elif param_type == WorkflowContext:
                    params.append(context)
                else:
                    params.append(_input)

        output = rpc_info.method_func(*params)

        pubs = communication.get_to_publishing_internal_channel()
        response = WorkflowWorkerRpcResponse(
            output=self._options.object_encoder.encode(output)
        )

        if len(pubs) > 0:
            response.publish_to_inter_state_channel = pubs
        if len(data_attributes.get_updated_values_to_return()) > 0:
            response.upsert_data_attributes = [
                KeyValue(k, v)
                for (k, v) in data_attributes.get_updated_values_to_return().items()
            ]
        upsert_sas = _create_upsert_search_attributes(
            search_attributes_types,
            search_attributes.get_upsert_to_server_int64_attribute_map(),
            search_attributes.get_upsert_to_server_string_attribute_map(),
            search_attributes.get_upsert_to_server_bool_attribute_map(),
            search_attributes.get_upsert_to_server_double_attribute_map(),
            search_attributes.get_upsert_to_server_string_array_attribute_map(),
        )
        if upsert_sas:
            response.upsert_search_attributes = upsert_sas
        if len(communication.get_to_trigger_state_movements()) > 0:
            movements = communication.get_to_trigger_state_movements()
            decision = StateDecision.multi_next_states(*movements)
            response.state_decision = _to_idl_state_decision(
                decision,
                wf_type,
                self._registry,
                self._options.object_encoder,
            )
        return response

    def handle_workflow_state_wait_until(
        self,
        request: WorkflowStateWaitUntilRequest,
    ) -> WorkflowStateWaitUntilResponse:
        wf_type = request.workflow_type
        state = self._registry.get_workflow_state_with_check(
            wf_type, request.workflow_state_id
        )
        internal_channel_types = self._registry.get_internal_channel_type_store(wf_type)
        signal_channel_types = self._registry.get_signal_channel_types(wf_type)
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

        data_attributes = DataAttributes(
            data_attributes_types, self._options.object_encoder, current_data_attributes
        )

        search_attributes_types = self._registry.get_search_attribute_types(wf_type)
        search_attributes = SearchAttributes(
            search_attributes_types, unset_to_none(request.search_attributes)
        )

        persistence = Persistence(data_attributes, search_attributes)

        communication = Communication(
            internal_channel_types,
            signal_channel_types,
            self._options.object_encoder,
            None,
            None,
        )
        command_request = state.wait_until(context, _input, persistence, communication)

        pubs = communication.get_to_publishing_internal_channel()

        upsert_sas = _create_upsert_search_attributes(
            search_attributes_types,
            search_attributes.get_upsert_to_server_int64_attribute_map(),
            search_attributes.get_upsert_to_server_string_attribute_map(),
            search_attributes.get_upsert_to_server_bool_attribute_map(),
            search_attributes.get_upsert_to_server_double_attribute_map(),
            search_attributes.get_upsert_to_server_string_array_attribute_map(),
        )

        response = WorkflowStateWaitUntilResponse(
            command_request=_to_idl_command_request(command_request),
            publish_to_inter_state_channel=pubs,
            upsert_data_objects=[
                KeyValue(k, v)
                for (k, v) in data_attributes.get_updated_values_to_return().items()
            ],
        )

        if upsert_sas:
            response.upsert_search_attributes = upsert_sas

        return response

    def handle_workflow_state_execute(
        self,
        request: WorkflowStateExecuteRequest,
    ) -> WorkflowStateExecuteResponse:
        wf_type = request.workflow_type
        state = self._registry.get_workflow_state_with_check(
            wf_type, request.workflow_state_id
        )
        internal_channel_types = self._registry.get_internal_channel_type_store(wf_type)
        signal_channel_types = self._registry.get_signal_channel_types(wf_type)
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

        data_attributes = DataAttributes(
            data_attributes_types, self._options.object_encoder, current_data_attributes
        )

        search_attributes_types = self._registry.get_search_attribute_types(wf_type)
        search_attributes = SearchAttributes(
            search_attributes_types, unset_to_none(request.search_attributes)
        )

        persistence = Persistence(data_attributes, search_attributes)

        communication = Communication(
            internal_channel_types,
            signal_channel_types,
            self._options.object_encoder,
            None,
            None,
        )

        command_results = from_idl_command_results(
            request.command_results,
            internal_channel_types,
            signal_channel_types,
            self._options.object_encoder,
        )
        decision = state.execute(
            context, _input, command_results, persistence, communication
        )

        pubs = communication.get_to_publishing_internal_channel()

        upsert_sas = _create_upsert_search_attributes(
            search_attributes_types,
            search_attributes.get_upsert_to_server_int64_attribute_map(),
            search_attributes.get_upsert_to_server_string_attribute_map(),
            search_attributes.get_upsert_to_server_bool_attribute_map(),
            search_attributes.get_upsert_to_server_double_attribute_map(),
            search_attributes.get_upsert_to_server_string_array_attribute_map(),
        )

        response = WorkflowStateExecuteResponse(
            state_decision=_to_idl_state_decision(
                decision,
                wf_type,
                self._registry,
                self._options.object_encoder,
            ),
            publish_to_inter_state_channel=pubs,
            upsert_data_objects=[
                KeyValue(k, v)
                for (k, v) in data_attributes.get_updated_values_to_return().items()
            ],
        )

        if upsert_sas:
            response.upsert_search_attributes = upsert_sas

        return response


def _create_upsert_search_attributes(
    type_map: dict[str, SearchAttributeValueType],
    upsert_to_server_int64_attribute_map: dict[str, Union[int, None]],
    upsert_to_server_keyword_attribute_map: dict[str, Union[str, None]],
    upsert_to_server_bool_attribute_map: dict[str, Union[bool, None]],
    upsert_to_server_double_attribute_map: dict[str, Union[float, None]],
    upsert_to_server_string_array_attribute_map: dict[str, Union[list[str], None]],
):
    sas: list[SearchAttribute] = []
    for int_key, int_sa in upsert_to_server_int64_attribute_map.items():
        sa = SearchAttribute(
            key=int_key,
            value_type=type_map[int_key],
        )
        if int_sa is not None:
            sa.integer_value = int_sa
        sas.append(sa)

    for keyword_key, keyword_sa in upsert_to_server_keyword_attribute_map.items():
        sa = SearchAttribute(
            key=keyword_key,
            value_type=type_map[keyword_key],
        )
        if keyword_sa is not None:
            sa.string_value = keyword_sa
        sas.append(sa)

    for bool_key, bool_sa in upsert_to_server_bool_attribute_map.items():
        sa = SearchAttribute(
            key=bool_key,
            value_type=type_map[bool_key],
        )
        if bool_sa is not None:
            sa.bool_value = bool_sa
        sas.append(sa)

    for double_key, double_sa in upsert_to_server_double_attribute_map.items():
        sa = SearchAttribute(
            key=double_key,
            value_type=type_map[double_key],
        )
        if double_sa is not None:
            sa.double_value = double_sa
        sas.append(sa)

    for (
        string_array_key,
        string_array_sa,
    ) in upsert_to_server_string_array_attribute_map.items():
        sa = SearchAttribute(
            key=string_array_key,
            value_type=type_map[string_array_key],
        )
        if string_array_sa is not None:
            sa.string_array_value = string_array_sa
        sas.append(sa)

    return sas
