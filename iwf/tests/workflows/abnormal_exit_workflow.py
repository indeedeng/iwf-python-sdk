from typing import Union

from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.iwf_api.models import RetryPolicy
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState
from iwf.workflow_state_options import WorkflowStateOptions


class AbnormalExitState1(WorkflowState[Union[int, str]]):
    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        raise RuntimeError("abnormal exit state")

    def get_state_options(self) -> WorkflowStateOptions:
        return WorkflowStateOptions(
            execute_api_retry_policy=RetryPolicy(maximum_attempts=1)
        )


class AbnormalExitWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(AbnormalExitState1())
