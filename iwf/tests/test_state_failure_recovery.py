import inspect
import time
import unittest

from iwf.client import Client
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.iwf_api.models import RetryPolicy
from iwf.iwf_api.models.wait_until_api_failure_policy import WaitUntilApiFailurePolicy
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState
from iwf.workflow_state_options import WorkflowStateOptions


class FailWaitUntilState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ):
        raise RuntimeError("failed wait_until")

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ):
        return StateDecision.single_next_state(FailExecuteState)

    def get_state_options(self) -> WorkflowStateOptions:
        return WorkflowStateOptions(
            execute_api_retry_policy=RetryPolicy(maximum_attempts=1),
            wait_until_api_retry_policy=RetryPolicy(maximum_attempts=1),
            proceed_to_execute_when_wait_until_retry_exhausted=WaitUntilApiFailurePolicy.PROCEED_ON_FAILURE,
        )


class FailExecuteState(WorkflowState[None]):
    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        raise RuntimeError("a random error to fail the state")

    def get_state_options(self) -> WorkflowStateOptions:
        return WorkflowStateOptions(
            execute_api_retry_policy=RetryPolicy(maximum_attempts=1),
            proceed_to_state_when_execute_retry_exhausted=RecoveryState,
        )


class RecoveryState(WorkflowState[None]):
    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return StateDecision.graceful_complete_workflow("done")


class RecoveryWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(
            FailWaitUntilState(), FailExecuteState(), RecoveryState()
        )


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = RecoveryWorkflow()
        registry.add_workflow(wf)
        cls.client = Client(registry)

    def test_workflow_recovery(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.client.start_workflow(RecoveryWorkflow, wf_id, 10)
        result = self.client.wait_for_workflow_completion(wf_id, str)
        assert result == "done"
