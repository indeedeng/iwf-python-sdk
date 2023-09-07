import inspect
import time
from typing import Union

from iwf.client import Client
from iwf.command_request import CommandRequest
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState


class State1(WorkflowState[Union[int, str]]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        if input != "input":
            raise RuntimeError("input is incorrect")
        return CommandRequest.empty()

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        if input != "input":
            raise RuntimeError("input is incorrect")
        return StateDecision.single_next_state(State2)


class State2(WorkflowState[None]):
    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return StateDecision.graceful_complete_workflow("done")


class BasicWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(State1(), State2())


hello_wf = BasicWorkflow()
registry.add_workflow(hello_wf)
client = Client(registry)


def test_basic_workflow():
    wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

    client.start_workflow(BasicWorkflow, wf_id, 100, "input")
    res = client.get_simple_workflow_result_with_wait(wf_id, str)
    assert res == "done"
