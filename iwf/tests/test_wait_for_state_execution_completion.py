import inspect
import time
import unittest

from iwf.client import Client
from iwf.command_request import CommandRequest, TimerCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_options import WorkflowOptions
from iwf.workflow_state import T, WorkflowState


class WaitForStateWithStateExecutionIdState1(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(2),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return StateDecision.single_next_state(WaitForStateWithStateExecutionIdState2)


class WaitForStateWithStateExecutionIdState2(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(2),
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


class WaitForStateWithStateExecutionIdWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(
            WaitForStateWithStateExecutionIdState1(),
            WaitForStateWithStateExecutionIdState2(),
        )


class TestWaitForStateWithStateExecutionId(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = WaitForStateWithStateExecutionIdWorkflow()
        registry.add_workflow(wf)
        cls.client = Client(registry)

    def test_wait_for_state_with_state_execution_id_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        wf_opts = WorkflowOptions()
        wf_opts.add_wait_for_completion_state_ids(
            WaitForStateWithStateExecutionIdState1
        )

        self.client.start_workflow(
            WaitForStateWithStateExecutionIdWorkflow, wf_id, 100, None, wf_opts
        )

        self.client.wait_for_state_execution_completion_with_state_execution_id(
            WaitForStateWithStateExecutionIdState1, wf_id
        )

        self.client.wait_for_workflow_completion(wf_id)

        # TODO: Improve this test by verifying both workflows completed with describe_workflow method
        # https://github.com/indeedeng/iwf-python-sdk/issues/22
        #
        # child_wf_id =
        #
        # wf_info = self.client.describe_workflow(wf_id);
        # assert wf_info.workflow_status == WorkflowStatus.COMPLETED
        #
        # child_wf_info = self.client.describe_workflow(child_wf_id);
        # assert child_wf_info.workflow_status == WorkflowStatus.COMPLETED


class WaitForStateWithWaitForKeyState1(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(2),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return StateDecision.single_next_state(
            WaitForStateWithWaitForKeyState2, None, None, "testKey"
        )


class WaitForStateWithWaitForKeyState2(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(2),
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


class WaitForStateWithWaitForKeyWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(
            WaitForStateWithWaitForKeyState1(), WaitForStateWithWaitForKeyState2()
        )


class TestWaitForStateWithWaitForKey(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = WaitForStateWithWaitForKeyWorkflow()
        registry.add_workflow(wf)
        cls.client = Client(registry)

    def test_wait_for_state_with_wait_for_key_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        wf_opts = WorkflowOptions()
        wf_opts.add_wait_for_completion_state_ids(WaitForStateWithWaitForKeyState2)

        self.client.start_workflow(
            WaitForStateWithWaitForKeyWorkflow, wf_id, 100, None, wf_opts
        )

        self.client.wait_for_state_execution_completion_with_wait_for_key(
            WaitForStateWithWaitForKeyState2, wf_id, "testKey"
        )

        self.client.wait_for_workflow_completion(wf_id)

        # TODO: Improve this test by verifying both workflows completed with describe_workflow method
        # https://github.com/indeedeng/iwf-python-sdk/issues/22
        #
        # child_wf_id =
        #
        # wf_info = self.client.describe_workflow(wf_id);
        # assert wf_info.workflow_status == WorkflowStatus.COMPLETED
        #
        # child_wf_info = self.client.describe_workflow(child_wf_id);
        # assert child_wf_info.workflow_status == WorkflowStatus.COMPLETED
