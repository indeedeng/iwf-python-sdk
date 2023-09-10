from typing import Any, Optional, Type, TypeVar

from iwf.client_options import ClientOptions
from iwf.registry import Registry
from iwf.stop_workflow_options import StopWorkflowOptions
from iwf.unregistered_client import UnregisteredClient, UnregisteredWorkflowOptions
from iwf.workflow import ObjectWorkflow, get_workflow_type_by_class
from iwf.workflow_options import WorkflowOptions
from iwf.workflow_state import get_state_id, should_skip_wait_until
from iwf.workflow_state_options import _to_idl_state_options

T = TypeVar("T")


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

    def get_simple_workflow_result_with_wait(
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
