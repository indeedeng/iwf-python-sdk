from typing import Any

from iwf.client_options import ClientOptions
from iwf.errors import InvalidArgumentError
from iwf.registry import Registry
from iwf.unregistered_client import UnregisteredClient, UnregisteredWorkflowOptions
from iwf.workflow import ObjectWorkflow, get_workflow_type
from iwf.workflow_options import WorkflowOptions
from iwf.workflow_state import get_state_id
from iwf.workflow_state_options import WorkflowStateOptions, to_idl_state_options


class Client:
    def __init__(self, registry: Registry, options: ClientOptions):
        self._registry = registry
        self._options = options
        self._unregistered_client = UnregisteredClient(options)

    async def start_workflow(
        self,
        wf: ObjectWorkflow,
        wf_id: str,
        timeout_seconds: int,
        input: Any = None,
        options: WorkflowOptions = None,
    ):
        wf_type = get_workflow_type(wf)
        wf = self._registry.get_workflow(wf_type)
        if wf is None:
            raise InvalidArgumentError("workflow {} is not registered".format(wf_type))

        starting_state_def = self._registry.get_workflow_starting_state_def(wf_type)
        unreg_opts = UnregisteredWorkflowOptions()
        starting_state_id = None

        if starting_state_def is not None:
            starting_state_id = get_state_id(starting_state_def.state)
            starting_state_opts = to_idl_state_options(starting_state_def.state.get_state_options())

            if should_skip_wait_until(starting_state_def.state):
                if starting_state_opts is None:
                    starting_state_opts = WorkflowStateOptions()
                    starting_state_opts.execute_api_timeout_seconds = 2
