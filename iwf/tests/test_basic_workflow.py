import inspect
import time
import unittest
from typing import Union

from iwf.client import Client
from iwf.command_request import CommandRequest, TimerCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.errors import WorkflowAlreadyStartedError
from iwf.iwf_api.models import WorkflowAlreadyStartedOptions
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_options import WorkflowOptions
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
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(1),
        )

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


class TestWorkflowErrors(unittest.TestCase):
    def test_basic_workflow(self):
        original_request_id = "1"
        later_request_id = "2"

        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        workflow_already_started_options_1 = WorkflowAlreadyStartedOptions(
            ignore_already_started_error=True
        )
        workflow_already_started_options_1.request_id = original_request_id

        start_options_1 = WorkflowOptions()
        start_options_1.workflow_already_started_options = (
            workflow_already_started_options_1
        )

        wf_run_id = client.start_workflow(
            BasicWorkflow, wf_id, 100, "input", start_options_1
        )
        assert wf_run_id

        wf_run_id = client.start_workflow(
            BasicWorkflow, wf_id, 100, "input", start_options_1
        )
        assert wf_run_id

        workflow_already_started_options_2 = WorkflowAlreadyStartedOptions(
            ignore_already_started_error=True
        )
        workflow_already_started_options_2.request_id = later_request_id

        start_options_2 = WorkflowOptions()
        start_options_2.workflow_already_started_option = (
            workflow_already_started_options_2
        )

        with self.assertRaises(WorkflowAlreadyStartedError):
            wf_run_id = client.start_workflow(
                BasicWorkflow, wf_id, 100, "input", start_options_2
            )
            assert wf_run_id

        res = client.wait_for_workflow_completion(wf_id, str)
        assert res == "done"
