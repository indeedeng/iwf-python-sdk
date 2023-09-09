import http
from dataclasses import dataclass
from typing import Any, List, Optional, Type, TypeVar

from iwf_api import Client
from iwf_api.api.default import (
    post_api_v1_workflow_dataobjects_get,
    post_api_v1_workflow_reset,
    post_api_v1_workflow_search,
    post_api_v1_workflow_searchattributes_get,
    post_api_v1_workflow_signal,
    post_api_v1_workflow_start,
    post_api_v1_workflow_stop,
    post_api_v1_workflow_timer_skip,
    post_api_v_1_workflow_get_with_wait,
)
from iwf_api.models import (
    EncodedObject,
    ErrorResponse,
    IDReusePolicy,
    SearchAttribute,
    SearchAttributeKeyAndType,
    WorkflowConfig,
    WorkflowGetDataObjectsRequest,
    WorkflowGetRequest,
    WorkflowGetResponse,
    WorkflowGetSearchAttributesRequest,
    WorkflowGetSearchAttributesResponse,
    WorkflowResetRequest,
    WorkflowRetryPolicy,
    WorkflowSearchRequest,
    WorkflowSearchResponse,
    WorkflowSignalRequest,
    WorkflowSkipTimerRequest,
    WorkflowStartOptions,
    WorkflowStartRequest,
    WorkflowStateOptions,
    WorkflowStatus,
    WorkflowStopRequest,
)
from iwf_api.types import Response

from iwf.client_options import ClientOptions
from iwf.errors import (
    WorkflowDefinitionError,
    process_http_error,
    process_http_error_get_api,
    process_workflow_abnormal_exit_error,
)
from iwf.reset_workflow_type_and_options import ResetWorkflowTypeAndOptions
from iwf.stop_workflow_options import StopWorkflowOptions


@dataclass
class UnregisteredWorkflowOptions:
    workflow_id_reuse_policy: Optional[IDReusePolicy] = None
    cron_schedule: Optional[str] = None
    workflow_retry_policy: Optional[WorkflowRetryPolicy] = None
    start_state_options: Optional[WorkflowStateOptions] = None
    initial_search_attribute: Optional[List[SearchAttribute]] = None
    workflow_config_override: Optional[WorkflowConfig] = None


T = TypeVar("T")


class UnregisteredClient:
    def __init__(self, client_options: ClientOptions):
        self.client_options = client_options
        self.api_client = Client(base_url=client_options.server_url, timeout=60)

    def start_workflow(
        self,
        workflow_type: str,
        workflow_id: str,
        start_state_id: Optional[str],
        workflow_timeout_seconds: int,
        input: Optional[Any],
        options: Optional[UnregisteredWorkflowOptions],
    ) -> str:
        request = WorkflowStartRequest(
            workflow_id=workflow_id,
            iwf_worker_url=self.client_options.worker_url,
            iwf_workflow_type=workflow_type,
            workflow_timeout_seconds=workflow_timeout_seconds,
            state_input=self.client_options.object_encoder.encode(input),
        )
        if start_state_id:
            request.start_state_id = start_state_id

        if options:
            if options.start_state_options:
                request.state_options = options.start_state_options

            start_options = WorkflowStartOptions()
            if options.workflow_id_reuse_policy:
                start_options.id_reuse_policy = options.workflow_id_reuse_policy
            if options.cron_schedule:
                start_options.cron_schedule = options.cron_schedule
            if options.workflow_retry_policy:
                start_options.retry_policy = options.workflow_retry_policy

            if options.workflow_config_override:
                start_options.workflow_config_override = (
                    options.workflow_config_override
                )
            request.workflow_start_options = start_options

        response = post_api_v1_workflow_start.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        return handler_error_and_return(response)

    def get_simple_workflow_result_with_wait(
        self,
        workflow_id: str,
        workflow_run_id: str,
        type_hint: Optional[Type[T]] = None,
    ) -> Optional[T]:
        """For most cases, a workflow only has one result(one completion state)
        Use this API to retrieve the output of the state"""
        request = WorkflowGetRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            needs_results=True,
        )
        response = post_api_v_1_workflow_get_with_wait.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        if response.status_code != http.HTTPStatus.OK:
            assert isinstance(response.parsed, ErrorResponse)
            raise process_http_error_get_api(response.status_code, response.parsed)

        parsed = response.parsed
        assert isinstance(parsed, WorkflowGetResponse)
        if parsed.workflow_status != WorkflowStatus.COMPLETED:
            raise process_workflow_abnormal_exit_error(parsed)

        if not parsed.results or len(parsed.results) == 0:
            return None
        filtered_results = [
            result for result in parsed.results if result.completed_state_output
        ]
        if len(filtered_results) == 0:
            return None
        elif len(filtered_results) == 1:
            result = filtered_results[0]
        else:
            raise WorkflowDefinitionError(
                "workflow must have one or zero state output for using this API"
            )

        assert isinstance(result.completed_state_output, EncodedObject)
        return self.client_options.object_encoder.decode(
            result.completed_state_output,
            type_hint,
        )

    def signal_workflow(
        self,
        workflow_id: str,
        workflow_run_id: str,
        signal_channel_name: str,
        signal_value: Optional[Any],
    ) -> None:
        request = WorkflowSignalRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            signal_channel_name=signal_channel_name,
            signal_value=self.client_options.object_encoder.encode(signal_value),
        )

        response = post_api_v1_workflow_signal.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        return handler_error_and_return(response)

    def reset_workflow(
        self,
        workflow_id: str,
        workflow_run_id: str,
        reset_workflow_type_and_options: ResetWorkflowTypeAndOptions,
    ) -> None:
        request = WorkflowResetRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            reset_type=reset_workflow_type_and_options.reset_type,
            reason=reset_workflow_type_and_options.reason,
        )
        if reset_workflow_type_and_options.history_event_id:
            request.history_event_id = reset_workflow_type_and_options.history_event_id
        if reset_workflow_type_and_options.history_event_time:
            request.history_event_time = (
                reset_workflow_type_and_options.history_event_time
            )
        if reset_workflow_type_and_options.state_id:
            request.state_id = reset_workflow_type_and_options.state_id
        if reset_workflow_type_and_options.state_execution_id:
            request.state_execution_id = (
                reset_workflow_type_and_options.state_execution_id
            )
        if reset_workflow_type_and_options.skip_signal_reapply:
            request.skip_signal_reapply = (
                reset_workflow_type_and_options.skip_signal_reapply
            )

        response = post_api_v1_workflow_reset.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        return handler_error_and_return(response)

    def skip_timer(
        self,
        workflow_id: str,
        workflow_run_id: str,
        workflow_state_id: str,
        state_execution_number: int,
        timer_command_id: str,
    ):
        request = WorkflowSkipTimerRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            workflow_state_execution_id=f"{workflow_state_id}-{state_execution_number}",
            timer_command_id=timer_command_id,
        )
        response = post_api_v1_workflow_timer_skip.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        return handler_error_and_return(response)

    def skip_timer_at_command_index(
        self,
        workflow_id: str,
        workflow_run_id: str,
        workflow_state_id: str,
        state_execution_number: int,
        timer_command_index: int,
    ) -> None:
        request = WorkflowSkipTimerRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            workflow_state_execution_id=f"{workflow_state_id}-{state_execution_number}",
            timer_command_index=timer_command_index,
        )
        response = post_api_v1_workflow_timer_skip.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        return handler_error_and_return(response)

    def stop_workflow(
        self,
        workflow_id: str,
        workflow_run_id: str,
        options: Optional[StopWorkflowOptions] = None,
    ):
        request = WorkflowStopRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
        )
        if options:
            request.stop_type = options.workflow_stop_type
            request.reason = options.reason
        response = post_api_v1_workflow_stop.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        return handler_error_and_return(response)

    def get_workflow_data_attributes(
        self,
        workflow_id: str,
        workflow_run_id: str,
        attribute_keys: Optional[List[str]] = None,
    ):
        request = WorkflowGetDataObjectsRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
        )
        if attribute_keys:
            request.keys = attribute_keys
        response = post_api_v1_workflow_dataobjects_get.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        return handler_error_and_return(response)

    def search_workflow(
        self,
        request: WorkflowSearchRequest,
    ) -> WorkflowSearchResponse:
        response = post_api_v1_workflow_search.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        return handler_error_and_return(response)

    def get_workflow_search_attributes(
        self,
        workflow_id: str,
        workflow_run_id: str,
        attribute_keys: Optional[List[SearchAttributeKeyAndType]] = None,
    ) -> WorkflowGetSearchAttributesResponse:
        request = WorkflowGetSearchAttributesRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
        )
        if attribute_keys:
            request.keys = attribute_keys
        response = post_api_v1_workflow_searchattributes_get.sync_detailed(
            client=self.api_client,
            json_body=request,
        )
        return handler_error_and_return(response)


def handler_error_and_return(response: Response):
    if response.status_code != http.HTTPStatus.OK:
        assert isinstance(response.parsed, ErrorResponse)
        raise process_http_error(response.status_code, response.parsed)
    return response.parsed
