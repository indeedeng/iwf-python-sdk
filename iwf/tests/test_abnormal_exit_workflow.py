import inspect
import time
import unittest
from typing import Union

from iwf.client import Client
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.errors import WorkflowFailed
from iwf.iwf_api.models import RetryPolicy
from iwf.iwf_api.models.id_reuse_policy import IDReusePolicy
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.test_basic_workflow import BasicWorkflow
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_options import WorkflowOptions
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


abnormal_exit_wf = AbnormalExitWorkflow()
registry.add_workflow(abnormal_exit_wf)
client = Client(registry)


class TestAbnormalWorkflow(unittest.TestCase):
    def test_abnormal_exit_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        startOptions = WorkflowOptions(
            workflow_id_reuse_policy=IDReusePolicy.ALLOW_IF_PREVIOUS_EXITS_ABNORMALLY
        )

        client.start_workflow(AbnormalExitWorkflow, wf_id, 100, "input", startOptions)
        with self.assertRaises(WorkflowFailed):
            client.get_simple_workflow_result_with_wait(wf_id, str)

        # Starting a workflow with the same ID should be allowed since the previous failed abnormally
        client.start_workflow(BasicWorkflow, wf_id, 100, "input", startOptions)
        res = client.get_simple_workflow_result_with_wait(wf_id, str)
        assert res == "done"
