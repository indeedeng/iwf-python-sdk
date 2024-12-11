import inspect
from typing import Any, Callable, Optional, Type, TypeVar, Union

from typing_extensions import deprecated

from iwf.client_options import ClientOptions
from iwf.errors import InvalidArgumentError
from iwf.registry import Registry
from iwf.reset_workflow_type_and_options import ResetWorkflowTypeAndOptions
from iwf.stop_workflow_options import StopWorkflowOptions
from iwf.unregistered_client import UnregisteredClient, UnregisteredWorkflowOptions
from iwf.workflow import ObjectWorkflow, get_workflow_type_by_class
from iwf.workflow_options import WorkflowOptions
from iwf.workflow_state import (
    WorkflowState,
    get_state_id,
    get_state_id_by_class,
    should_skip_wait_until,
)
from iwf.workflow_state_options import _to_idl_state_options

T = TypeVar("T")


def get_workflow_type_by_rpc_method(meth) -> str:
    if inspect.ismethod(meth):
        return inspect.getmro(meth.__self__.__class__)[0].__name__
    if inspect.isfunction(meth):
        return meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0]
    raise InvalidArgumentError(f"method {meth} is not a RPC method")


class Client:
    def __init__(self, registry: Registry, options: Optional[ClientOptions] = None):
        self._registry = registry
        if options is None:
            options = ClientOptions.local_default()
        self._options = options
        self._unregistered_client = UnregisteredClient(options)

    def start_workflow(
        self,
        wf_class: type[ObjectWorkflow],
        wf_id: str,
        timeout_seconds: int,
        input: Any = None,
        options: Optional[WorkflowOptions] = None,
    ) -> None:
        """

        Args:
            wf_class: the workflow definition class
            wf_id: workflowId
            timeout_seconds: the timeout. Use zero for infinite timeout(only works for Temporal as backend)
            input: input of the workflow, aka, the input of the starting state of the workflow
            options: advanced options

        Raises:
            ClientSideError for non-retryable error
            ServerSideError for server error
        """
        wf_type = get_workflow_type_by_class(wf_class)
        self._registry.get_workflow_with_check(wf_type)

        starting_state = self._registry.get_workflow_starting_state(wf_type)
        unreg_opts = UnregisteredWorkflowOptions()

        if options is not None:
            unreg_opts.workflow_id_reuse_policy = options.workflow_id_reuse_policy
            unreg_opts.workflow_retry_policy = options.workflow_retry_policy
            unreg_opts.cron_schedule = options.workflow_cron_schedule
            unreg_opts.workflow_start_delay_seconds = (
                options.workflow_start_delay_seconds
            )
            unreg_opts.workflow_already_started_options = (
                options.workflow_already_started_options
            )
            unreg_opts.initial_data_attributes = options.initial_data_attributes

            unreg_opts.workflow_config_override = options.workflow_config_override

            # TODO: set initial search attributes here

        starting_state_id = None

        if starting_state is not None:
            starting_state_id = get_state_id(starting_state)
            starting_state_opts = _to_idl_state_options(
                should_skip_wait_until(starting_state),
                starting_state.get_state_options(),
                self._registry.get_state_store(wf_type),
            )
            unreg_opts.start_state_options = starting_state_opts

        self._unregistered_client.start_workflow(
            wf_type, wf_id, starting_state_id, timeout_seconds, input, unreg_opts
        )

    @deprecated("use wait_for_workflow_completion instead")
    def get_simple_workflow_result_with_wait(
        self,
        workflow_id: str,
        type_hint: Optional[Type[T]] = None,
    ) -> Optional[T]:
        return self._unregistered_client.get_simple_workflow_result_with_wait(
            workflow_id, "", type_hint
        )

    def wait_for_workflow_completion(
        self,
        workflow_id: str,
        type_hint: Optional[Type[T]] = None,
    ) -> Optional[T]:
        """
        This will be waiting up to 5~60 seconds (configurable in HTTP client and capped by server) for workflow to
        complete, and return the workflow completion result.
        Args:
            workflow_id: workflowId
            type_hint:  the type of workflow result

        Returns:
            the completion result if there is one
        Raises
            WorkflowAbnormalExitError if workflow failed/timeout/canceled/terminated
            WorkflowStillRunningError if workflow is still running after exceeding the waiting timeout(HTTP timeout)
            ClientSideError for non-retryable error
            ServerSideError for server error
        """
        return self._unregistered_client.get_simple_workflow_result_with_wait(
            workflow_id, "", type_hint
        )

    def stop_workflow(
        self,
        workflow_id: str,
        options: Optional[StopWorkflowOptions] = None,
    ):
        return self._unregistered_client.stop_workflow(workflow_id, "", options)

    def invoke_rpc(
        self,
        workflow_id: str,
        rpc: Callable,  # this can be a function: RPCWorkflow.rpc_method or a method: workflow_instance.rpc_method
        input: Any = None,
        return_type_hint: Optional[Type[T]] = None,
    ) -> Optional[T]:
        wf_type = get_workflow_type_by_rpc_method(rpc)
        rpc_name = rpc.__name__
        rpc_info = self._registry.get_rpc_infos(wf_type)[rpc_name]

        return self._unregistered_client.invoke_rpc(
            input=input,
            workflow_id=workflow_id,
            workflow_run_id="",
            rpc_name=rpc_name,
            timeout_seconds=rpc_info.timeout_seconds,
            data_attribute_policy=rpc_info.data_attribute_loading_policy,
            all_defined_search_attribute_types=[],
            return_type_hint=return_type_hint,
        )

    def signal_workflow(
        self,
        workflow_id: str,
        signal_channel_name: str,
        signal_value: Optional[Any] = None,
    ):
        return self._unregistered_client.signal_workflow(
            workflow_id, "", signal_channel_name, signal_value
        )

    def reset_workflow(
        self,
        workflow_id: str,
        reset_workflow_type_and_options: ResetWorkflowTypeAndOptions,
    ):
        return self._unregistered_client.reset_workflow(
            workflow_id, "", reset_workflow_type_and_options
        )

    def skip_timer_by_command_id(
        self,
        workflow_id: str,
        workflow_state_id: str,
        timer_command_id: str,
        state_execution_number: int = 1,
    ):
        return self._unregistered_client.skip_timer_by_command_id(
            workflow_id,
            "",
            workflow_state_id,
            timer_command_id=timer_command_id,
            state_execution_number=state_execution_number,
        )

    def skip_timer_at_command_index(
        self,
        workflow_id: str,
        workflow_state_id: Union[str, type[WorkflowState]],
        state_execution_number: int = 1,
        timer_command_index: int = 0,
    ):
        if isinstance(workflow_state_id, type):
            state_id = get_state_id_by_class(workflow_state_id)
        else:
            state_id = workflow_state_id
        return self._unregistered_client.skip_timer_at_command_index(
            workflow_id,
            "",
            state_id,
            state_execution_number,
            timer_command_index,
        )
