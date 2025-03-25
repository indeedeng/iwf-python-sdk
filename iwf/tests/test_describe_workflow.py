import inspect
import time
import unittest

from iwf.client import Client
from iwf.command_request import CommandRequest, TimerCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.errors import WorkflowNotExistsError
from iwf.iwf_api.models import WorkflowStatus
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState


class WaitState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(10),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:

        return StateDecision.graceful_complete_workflow()


class DescribeWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(WaitState())


wf = DescribeWorkflow()
registry.add_workflow(wf)
client = Client(registry)


class TestDescribeWorkflow(unittest.TestCase):
    def test_describe_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        client.start_workflow(DescribeWorkflow, wf_id, 100)
        workflow_info = client.describe_workflow(wf_id)
        assert workflow_info.workflow_status == WorkflowStatus.RUNNING

        # Stop the workflow
        client.stop_workflow(wf_id)

    def test_describe_workflow_when_workflow_not_exists(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        with self.assertRaises(WorkflowNotExistsError):
            client.describe_workflow(wf_id)
