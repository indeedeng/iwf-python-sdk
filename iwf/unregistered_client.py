from typing import Any, List, Optional, Type

from iwf_api import Client
from iwf_api.api.default import (
    post_api_v1_workflow_dataobjects_get,
    post_api_v1_workflow_reset,
    post_api_v1_workflow_rpc,
    post_api_v1_workflow_search,
    post_api_v1_workflow_searchattributes_get,
    post_api_v1_workflow_signal,
    post_api_v1_workflow_start,
    post_api_v1_workflow_stop,
    post_api_v1_workflow_timer_skip,
    post_api_v_1_workflow_get_with_wait,
)
from iwf_api.models import (
    ErrorResponse,
    IDReusePolicy,
    PersistenceLoadingPolicy,
    SearchAttribute,
    SearchAttributeKeyAndType,
    StateCompletionOutput,
    WorkflowConfig,
    WorkflowGetDataObjectsRequest,
    WorkflowGetRequest,
    WorkflowGetSearchAttributesRequest,
    WorkflowGetSearchAttributesResponse,
    WorkflowResetRequest,
    WorkflowRetryPolicy,
    WorkflowRpcRequest,
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
from pydantic.main import BaseModel

from iwf.client_options import ClientOptions
from iwf.reset_workflow_type_and_options import ResetWorkflowTypeAndOptions
from iwf.stop_workflow_options import StopWorkflowOptions
from iwf.utils.client_utils import get_search_attribute_value


class UnregisteredWorkflowOptions(BaseModel):
    workflow_id_reuse_policy: Optional[IDReusePolicy]
    cron_schedule: Optional[str]
    workflow_retry_policy: Optional[WorkflowRetryPolicy]
    start_state_options: Optional[WorkflowStateOptions]
    initial_search_attribute: List[SearchAttribute] = []
    workflow_config_override: Optional[WorkflowConfig]


class UnregisteredClient:
    def __init__(self, client_options: ClientOptions):
        self.client_options = client_options
        self.api_client = Client(base_url=client_options.server_url)

    async def start_workflow(
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
            state_input=await self.client_options.converter.encode(input),
        )
        if start_state_id:
            request.start_state_id = start_state_id

        if options:
            start_options = WorkflowStartOptions()
            if options.workflow_id_reuse_policy:
                start_options.id_reuse_policy = options.workflow_id_reuse_policy
            if options.cron_schedule:
                start_options.cron_schedule = options.cron_schedule
            if options.workflow_retry_policy:
                start_options.retry_policy = options.workflow_retry_policy
            if options.start_state_options:
                request.state_options = options.start_state_options
            for search_attribute in options.initial_search_attribute:
                if not search_attribute.value_type:
                    raise Exception("value_type is required")
                value = get_search_attribute_value(
                    search_attribute.value_type,
                    search_attribute,
                )
                if not value:
                    raise Exception(
                        f"Search attribute value is not set correctly for key {search_attribute.key} with value type {search_attribute.value_type}",
                    )
            if options.initial_search_attribute:
                start_options.search_attributes = options.initial_search_attribute
            if options.workflow_config_override:
                start_options.workflow_config_override = (
                    options.workflow_config_override
                )
            request.workflow_start_options = start_options

        response = await post_api_v1_workflow_start.asyncio(
            client=self.api_client,
            json_body=request,
        )
        if isinstance(response, ErrorResponse):
            raise Exception(response.detail)
        return response.workflow_run_id

    async def get_simple_workflow_result_with_wait(
        self,
        workflow_id: str,
        workflow_run_id: str,
        type_hint: Optional[Type] = None,
    ):
        """For most cases, a workflow only has one result(one completion state)
        Use this API to retrieve the output of the state"""
        request = WorkflowGetRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            needs_results=True,
        )
        response = await post_api_v_1_workflow_get_with_wait.asyncio(
            client=self.api_client,
            json_body=request,
        )

        if response.workflow_status != WorkflowStatus.COMPLETED:
            raise Exception(f"Workflow {workflow_id} is not completed yet.")

        if not response.results or len(response.results) == 0:
            return None
        filtered_results = [
            result for result in response.results if result.completed_state_output
        ]
        # TODO: Make sure there is only one result
        if len(filtered_results) == 1:
            result = filtered_results[0]
        else:
            result = response.results[0]
        return await self.client_options.converter.decode(
            result.completed_state_output,
            type_hint,
        )

    async def get_complex_workflow_result_with_wait(
        self,
        workflow_id: str,
        workflow_run_id: Optional[str] = None,
    ) -> List[StateCompletionOutput]:
        request = WorkflowGetRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            needs_results=True,
        )
        response = await post_api_v_1_workflow_get_with_wait.asyncio(
            client=self.api_client,
            json_body=request,
        )
        if isinstance(response, ErrorResponse):
            raise Exception(response.detail)

        if response.workflow_status != WorkflowStatus.COMPLETED:
            raise Exception(f"Workflow {workflow_id} is not completed yet.")

        return response.results

    async def signal_workflow(
        self,
        workflow_id: str,
        workflow_run_id: str,
        signal_channel_name: str,
        signal_value: Any,
    ) -> None:
        request = WorkflowSignalRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            signal_channel_name=signal_channel_name,
            signal_value=await self.client_options.converter.encode(signal_value),
        )

        response = await post_api_v1_workflow_signal.asyncio(
            client=self.api_client,
            json_body=request,
        )
        if isinstance(response, ErrorResponse):
            raise Exception(response.detail)

    async def reset_workflow(
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

        response = await post_api_v1_workflow_reset.asyncio(
            client=self.api_client,
            json_body=request,
        )
        if isinstance(response, ErrorResponse):
            raise Exception(response.detail)

    async def skip_timer(
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
        return await post_api_v1_workflow_timer_skip.asyncio(
            client=self.api_client,
            json_body=request,
        )

    async def skip_timer_at_command_index(
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
        await post_api_v1_workflow_timer_skip.asyncio(
            client=self.api_client,
            json_body=request,
        )

    async def stop_workflow(
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
        return await post_api_v1_workflow_stop.asyncio(
            client=self.api_client,
            json_body=request,
        )

    async def get_any_workflow_data_objects(
        self,
        workflow_id: str,
        workflow_run_id: str,
        attribute_keys: List[str] = None,
    ):
        request = WorkflowGetDataObjectsRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            keys=attribute_keys,
        )
        return await post_api_v1_workflow_dataobjects_get.asyncio(
            client=self.api_client,
            json_body=request,
        )

    async def search_workflow(
        self,
        request: WorkflowSearchRequest,
    ) -> WorkflowSearchResponse:
        return await post_api_v1_workflow_search.asyncio(
            client=self.api_client,
            json_body=request,
        )

    async def invoke_rpc(
        self,
        input: Any,
        workflow_id: str,
        workflow_run_id: str,
        rpc_name: str,
        timeout_seconds: int,
        type_hint: Optional[Type] = None,
        data_attributes_loading_policy: Optional[PersistenceLoadingPolicy] = None,
        search_attributes_loading_policy: Optional[PersistenceLoadingPolicy] = None,
    ):
        request = WorkflowRpcRequest(
            input_=await self.client_options.converter.encode(input),
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            rpc_name=rpc_name,
            timeout_seconds=timeout_seconds,
        )
        if data_attributes_loading_policy:
            request.data_attributes_loading_policy = data_attributes_loading_policy
        if search_attributes_loading_policy:
            request.search_attributes_loading_policy = search_attributes_loading_policy
        response = await post_api_v1_workflow_rpc.asyncio(
            client=self.api_client,
            json_body=request,
        )
        return await self.client_options.converter.decode(
            response.output,
            type_hint,
        )

    async def get_any_workflow_search_attributes(
        self,
        workflow_id: str,
        workflow_run_id: str,
        attribute_keys: Optional[List[SearchAttributeKeyAndType]] = None,
    ) -> WorkflowGetSearchAttributesResponse:
        request = WorkflowGetSearchAttributesRequest(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            keys=attribute_keys,
        )
        return await post_api_v1_workflow_searchattributes_get.asyncio(
            client=self.api_client,
            json_body=request,
        )
