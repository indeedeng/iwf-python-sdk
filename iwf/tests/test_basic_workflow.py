import inspect
import time

from iwf.client import Client
from iwf.command_request import CommandRequest
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.persistence import Persistence
from iwf.state_decision import (
    StateDecision,
    graceful_complete_workflow,
    single_next_state,
)
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.utils.iwf_typing import NoneType
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import WorkflowState, T


class State1(WorkflowState[str]):
    def get_input_type(self) -> type[str]:
        return str

    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest()

    def execute(
        self,
        ctx: WorkflowContext,
        input: str,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return single_next_state(State2)


class State2(WorkflowState[None]):
    def get_input_type(self) -> type[T]:
        return NoneType

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return graceful_complete_workflow("done")


class BasicWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(State1(), State2())


hello_wf = BasicWorkflow()
registry.add_workflow(hello_wf)
client = Client(registry)


def test_start_workflow():
    wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

    client.start_workflow(BasicWorkflow, wf_id, 100)
    res = client.get_simple_workflow_result_with_wait(wf_id, str)
    assert res == "done"
