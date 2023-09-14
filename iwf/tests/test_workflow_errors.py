import inspect
import time
import unittest

from iwf.client import Client
from iwf.command_request import CommandRequest, InternalChannelCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.errors import (
    WorkflowAlreadyStartedError,
    WorkflowCanceled,
    WorkflowFailed,
    WorkflowNotExistsError,
    WorkflowStillRunningError,
    WorkflowTerminated,
    WorkflowTimeout,
)
from iwf.iwf_api.models import WorkflowStopType
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.stop_workflow_options import StopWorkflowOptions
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState

test_channel_name = "test-name"


class WaitState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            InternalChannelCommand.by_name(test_channel_name)
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


class WaitInternalChannelWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(WaitState())


wf = WaitInternalChannelWorkflow()
registry.add_workflow(wf)
client = Client(registry)


class TestWorkflowErrors(unittest.TestCase):
    def test_workflow_timeout(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        client.start_workflow(WaitInternalChannelWorkflow, wf_id, 1)
        with self.assertRaises(WorkflowTimeout):
            client.get_simple_workflow_result_with_wait(wf_id, str)
        with self.assertRaises(WorkflowNotExistsError):
            client.get_simple_workflow_result_with_wait("invalid_id", str)

    def test_workflow_still_running_when_wait(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        # client_options = ClientOptions.local_default()
        # client_options.api_timeout = 5
        # TODO using a shorter api timeout will throw a different timeout eror, it's better to unify it
        client.start_workflow(WaitInternalChannelWorkflow, wf_id, 61)

        with self.assertRaises(WorkflowAlreadyStartedError):
            client.start_workflow(WaitInternalChannelWorkflow, wf_id, 61)

        with self.assertRaises(WorkflowStillRunningError):
            client.get_simple_workflow_result_with_wait(wf_id, str)

    def test_workflow_canceled(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        client.start_workflow(WaitInternalChannelWorkflow, wf_id, 10)
        client.stop_workflow(wf_id)
        with self.assertRaises(WorkflowCanceled):
            client.get_simple_workflow_result_with_wait(wf_id, str)

    def test_workflow_terminated(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        client.start_workflow(WaitInternalChannelWorkflow, wf_id, 10)
        client.stop_workflow(
            wf_id,
            StopWorkflowOptions(
                workflow_stop_type=WorkflowStopType.TERMINATE, reason="test"
            ),
        )
        with self.assertRaises(WorkflowTerminated):
            client.get_simple_workflow_result_with_wait(wf_id, str)

    def test_workflow_failed(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        client.start_workflow(WaitInternalChannelWorkflow, wf_id, 10)
        client.stop_workflow(
            wf_id,
            StopWorkflowOptions(
                workflow_stop_type=WorkflowStopType.FAIL, reason="test"
            ),
        )
        with self.assertRaises(WorkflowFailed):
            client.get_simple_workflow_result_with_wait(wf_id, str)
