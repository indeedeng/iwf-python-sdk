import inspect
import time
import unittest

from iwf.client import Client
from iwf.command_request import CommandRequest
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.persistence_schema import PersistenceSchema, PersistenceField
from iwf.workflow_options import WorkflowOptions

from iwf.iwf_api.models import RetryPolicy, WaitUntilApiFailurePolicy, IDReusePolicy
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState
from iwf.workflow_state_options import WorkflowStateOptions

output_da = "output_da"


class InitState(WorkflowState[str]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        persistence.set_data_attribute(
            output_da, str(input) + "_InitState_waitUntil_completed"
        )
        return CommandRequest.empty()

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        data = persistence.get_data_attribute(output_da)
        data += "_InitState_execute_completed"
        return StateDecision.single_next_state(
            NonInitState,
            data,
            WorkflowStateOptions(
                wait_until_api_retry_policy=RetryPolicy(maximum_attempts=2),
                proceed_to_execute_when_wait_until_retry_exhausted=WaitUntilApiFailurePolicy.PROCEED_ON_FAILURE,
            ),
        )


class NonInitState(WorkflowState[str]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        raise RuntimeError("test failure")

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        data = str(input) + "_NonInitState_execute_completed"
        return StateDecision.graceful_complete_workflow(data)

    def get_state_options(self) -> WorkflowStateOptions:
        return WorkflowStateOptions(
            wait_until_api_retry_policy=RetryPolicy(maximum_attempts=1),
            proceed_to_execute_when_wait_until_retry_exhausted=WaitUntilApiFailurePolicy.FAIL_WORKFLOW_ON_FAILURE,
        )


class StateOptionsOverrideWorkflow(ObjectWorkflow):
    def get_persistence_schema(self) -> PersistenceSchema:
        return PersistenceSchema.create(
            PersistenceField.data_attribute_def(output_da, str),
        )

    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(InitState(), NonInitState())


class TestStateOptionsOverrideWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = StateOptionsOverrideWorkflow()
        registry.add_workflow(wf)
        cls.client = Client(registry)

    def test_override(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.client.start_workflow(
            StateOptionsOverrideWorkflow,
            wf_id,
            10,
            "input",
            WorkflowOptions(workflow_id_reuse_policy=IDReusePolicy.DISALLOW_REUSE),
        )
        output = self.client.wait_for_workflow_completion(wf_id)

        assert (
            output
            == "input_InitState_waitUntil_completed_InitState_execute_completed_NonInitState_execute_completed"
        )
