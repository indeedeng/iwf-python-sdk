import inspect
from typing import Any, Callable, Optional, Type, TypeVar, Union

from typing_extensions import deprecated

from iwf.client_options import ClientOptions
from iwf.errors import InvalidArgumentError
from iwf.iwf_api.models import (
    SearchAttribute,
    SearchAttributeKeyAndType,
    SearchAttributeValueType,
)
from iwf.iwf_api.types import Unset
from iwf.registry import Registry
from iwf.reset_workflow_type_and_options import ResetWorkflowTypeAndOptions
from iwf.stop_workflow_options import StopWorkflowOptions
from iwf.unregistered_client import UnregisteredClient, UnregisteredWorkflowOptions
from iwf.utils.iwf_typing import unset_to_none
from iwf.workflow import ObjectWorkflow, get_workflow_type_by_class
from iwf.workflow_options import WorkflowOptions
from iwf.workflow_state import (
    WorkflowState,
    get_state_id,
    get_state_id_by_class,
    get_state_execution_id,
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

            unreg_opts.wait_for_completion_state_ids = (
                options.wait_for_completion_state_ids
            )
            unreg_opts.wait_for_completion_state_execution_ids = (
                options.wait_for_completion_state_execution_ids
            )

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

    def get_all_search_attributes(
        self,
        workflow_class: type[ObjectWorkflow],
        workflow_id: str,
        workflow_run_id: Optional[str] = None,
    ):
        run_id = workflow_run_id if workflow_run_id is not None else ""

        return self._do_get_workflow_search_attributes(
            workflow_class, workflow_id, run_id
        )

    def get_workflow_search_attributes(
        self,
        workflow_class: type[ObjectWorkflow],
        workflow_id: str,
        attribute_keys: list[str],
        workflow_run_id: Optional[str] = None,
    ):
        if not attribute_keys:
            raise ValueError(
                "attribute_keys must contain at least one entry, or use get_all_search_attributes API to get all"
            )

        run_id = workflow_run_id if workflow_run_id is not None else ""

        return self._do_get_workflow_search_attributes(
            workflow_class, workflow_id, run_id, attribute_keys
        )

    def _do_get_workflow_search_attributes(
        self,
        workflow_class: type[ObjectWorkflow],
        workflow_id: str,
        workflow_run_id: str,
        attribute_keys: Optional[list[str]] = None,
    ):
        wf_type = get_workflow_type_by_class(workflow_class)
        self._registry.get_workflow_with_check(wf_type)

        search_attribute_types = self._registry.get_search_attribute_types(wf_type)

        # if attribute keys is None, will fetch all registered search attributes from the server
        if attribute_keys:
            non_existing_search_attribute_list: list[str] = []
            for attribute_key in attribute_keys:
                if attribute_key not in search_attribute_types:
                    non_existing_search_attribute_list.append(attribute_key)

            if non_existing_search_attribute_list:
                raise InvalidArgumentError(
                    f"Search attributes not registered: {','.join(non_existing_search_attribute_list)}"
                )

        key_and_types: list[SearchAttributeKeyAndType] = []
        if attribute_keys is None:
            for attribute_key, sa_type in search_attribute_types.items():
                key_and_types.append(SearchAttributeKeyAndType(attribute_key, sa_type))
        else:
            for attribute_key in attribute_keys:
                sa_type = search_attribute_types[attribute_key]
                key_and_types.append(SearchAttributeKeyAndType(attribute_key, sa_type))

        response = self._unregistered_client.get_workflow_search_attributes(
            workflow_id, workflow_run_id, key_and_types
        )

        response_sas = response.search_attributes

        # TODO: troubleshoot why unset_to_none doesn't work as expected with lists
        if isinstance(response_sas, Unset) or response_sas is None:
            raise RuntimeError("search attributes not returned")

        result: dict[str, Any] = {}

        for response_sa in response_sas:
            response_sa_key = unset_to_none(response_sa.key)
            if response_sa_key is None:
                raise RuntimeError("search attribute key is None")
            response_sa_type = search_attribute_types[response_sa_key]
            value = get_search_attribute_value(response_sa_type, response_sa)
            result[response_sa_key] = value

        return result

    def set_workflow_search_attributes(
        self,
        workflow_class: type[ObjectWorkflow],
        workflow_id: str,
        search_attributes: list[SearchAttribute],
        workflow_run_id: Optional[str] = None,
    ):
        run_id = workflow_run_id if workflow_run_id is not None else ""

        return self._do_set_workflow_search_attributes(
            workflow_class, workflow_id, run_id, search_attributes
        )

    """A long poll API to wait for the completion of the state.
    Note 1 The state_completion to wait for is needed to registered on starting workflow due to limitation in https://github.com/indeedeng/iwf/issues/349
    Note 2 The max polling time is configured in client_options (default to 10s)

    Args:
        state_class the state class.
        workflow_id the workflowId
        state_execution_number the state execution number. E.g. if it's 2, it means the 2nd execution of the state
    """

    def wait_for_state_execution_completion_with_state_execution_id(
        self,
        state_class: type[WorkflowState],
        workflow_id: str,
        state_execution_number: int = 1,
    ):
        state_execution_id = get_state_execution_id(state_class, state_execution_number)

        self._unregistered_client.wait_for_state_execution_completion_with_state_execution_id(
            workflow_id, state_execution_id
        )

    """A long poll API to wait for the completion of the state.
    Note 1 The state_completion to wait for is needed to registered on starting workflow due to limitation in https://github.com/indeedeng/iwf/issues/349
    Note 2 The max polling time is configured in client_options (default to 10s)

    Args:
        state_class the state class.
        workflow_id the workflowId
        wait_for_key key provided by the client and to identity workflow
    """

    def wait_for_state_execution_completion_with_wait_for_key(
        self, state_class: type[WorkflowState], workflow_id: str, wait_for_key: str
    ):
        state_id = get_state_id_by_class(state_class)

        self._unregistered_client.wait_for_state_execution_completion_with_wait_for_key(
            workflow_id, state_id, wait_for_key
        )

    def _do_set_workflow_search_attributes(
        self,
        workflow_class: type[ObjectWorkflow],
        workflow_id: str,
        workflow_run_id: str,
        search_attributes: list[SearchAttribute],
    ):
        wf_type = get_workflow_type_by_class(workflow_class)
        self._registry.get_workflow_with_check(wf_type)

        search_attribute_types = self._registry.get_search_attribute_types(wf_type)

        # Check that the requested sa type is registered to the key
        for search_attribute in search_attributes:
            sa_key = unset_to_none(search_attribute.key)
            if sa_key is None:
                raise RuntimeError("search attribute key is None")
            if sa_key not in search_attribute_types:
                raise InvalidArgumentError(f"Search attribute not registered: {sa_key}")
            registered_value_type = search_attribute_types[sa_key]

            sa_value_type = unset_to_none(search_attribute.value_type)
            if sa_value_type is None:
                raise RuntimeError("search value type is None")

            if (
                sa_value_type is not None
                and registered_value_type != sa_value_type.value
            ):
                raise ValueError(
                    f"Search attribute key, {sa_key} is registered to type {registered_value_type}, but tried to add search attribute type {sa_value_type.value}"
                )

        self._unregistered_client.set_workflow_search_attributes(
            workflow_id, workflow_run_id, search_attributes
        )


def get_search_attribute_value(
    sa_type: SearchAttributeValueType, attribute: SearchAttribute
):
    if (
        sa_type == SearchAttributeValueType.KEYWORD
        or sa_type == SearchAttributeValueType.DATETIME
        or sa_type == SearchAttributeValueType.TEXT
    ):
        return unset_to_none(attribute.string_value)
    elif sa_type == SearchAttributeValueType.INT:
        return unset_to_none(attribute.integer_value)
    elif sa_type == SearchAttributeValueType.DOUBLE:
        return unset_to_none(attribute.double_value)
    elif sa_type == SearchAttributeValueType.BOOL:
        return unset_to_none(attribute.bool_value)
    elif sa_type == SearchAttributeValueType.KEYWORD_ARRAY:
        return unset_to_none(attribute.string_array_value)
    else:
        raise ValueError(f"not supported search attribute value type, {sa_type}")
