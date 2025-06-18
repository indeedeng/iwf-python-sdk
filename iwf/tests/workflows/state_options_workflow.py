from iwf.command_request import CommandRequest
from iwf.command_results import CommandResults
from iwf.communication import Communication

from iwf.iwf_api.models import RetryPolicy, WaitUntilApiFailurePolicy
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState
from iwf.workflow_state_options import WorkflowStateOptions


class InitState1(WorkflowState[str]):
    def get_state_options(self) -> WorkflowStateOptions:
        return WorkflowStateOptions(
            wait_until_api_retry_policy=RetryPolicy(maximum_attempts=1),
            proceed_to_execute_when_wait_until_retry_exhausted=WaitUntilApiFailurePolicy.PROCEED_ON_FAILURE,
        )

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
        data = "InitState1_execute_completed"
        return StateDecision.graceful_complete_workflow(data)


class InitState2(WorkflowState[str]):
    def get_state_options(self) -> WorkflowStateOptions:
        return WorkflowStateOptions(
            wait_until_api_retry_policy=RetryPolicy(maximum_attempts=1),
            proceed_to_execute_when_wait_until_retry_exhausted=WaitUntilApiFailurePolicy.FAIL_WORKFLOW_ON_FAILURE,
        )

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
        data = "InitState2_execute_completed"
        return StateDecision.graceful_complete_workflow(data)


class StateOptionsWorkflow1(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(InitState1())


class StateOptionsWorkflow2(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(InitState2())
