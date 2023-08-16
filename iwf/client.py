from typing import Any, Optional

from iwf.client_options import ClientOptions
from iwf.registry import Registry
from iwf.unregistered_client import UnregisteredClient, UnregisteredWorkflowOptions
from iwf.workflow import ObjectWorkflow, get_workflow_type
from iwf.workflow_options import WorkflowOptions
from iwf.workflow_state import get_state_id, should_skip_wait_until
from iwf.workflow_state_options import to_idl_state_options


class Client:
    def __init__(self, registry: Registry, options: ClientOptions):
        self._registry = registry
        self._options = options
        self._unregistered_client = UnregisteredClient(options)

    def start_workflow(
        self,
        wf: ObjectWorkflow,
        wf_id: str,
        timeout_seconds: int,
        input: Any = None,
        options: Optional[WorkflowOptions] = None,
    ) -> str:
        wf_type = get_workflow_type(wf)
        wf = self._registry.get_workflow_with_check(wf_type)

        starting_state_def = self._registry.get_workflow_starting_state_def(wf_type)
        unreg_opts = (
            UnregisteredWorkflowOptions()
        )  # TODO Why Mypy is complaining with creating an empty data class??

        if options is not None:
            unreg_opts.workflow_id_reuse_policy = options.workflow_id_reuse_policy
            unreg_opts.workflow_retry_policy = options.workflow_retry_policy
            unreg_opts.cron_schedule = options.workflow_cron_schedule

            # TODO: set initial search attributes here

        starting_state_id = None

        if starting_state_def is not None:
            starting_state_id = get_state_id(starting_state_def.state)
            starting_state_opts = to_idl_state_options(
                starting_state_def.state.get_state_options()
            )

            if should_skip_wait_until(starting_state_def.state):
                starting_state_opts.skip_wait_until = True

            unreg_opts.start_state_options = starting_state_opts

        return self._unregistered_client.start_workflow(
            wf_type, wf_id, starting_state_id, timeout_seconds, input, unreg_opts
        )
