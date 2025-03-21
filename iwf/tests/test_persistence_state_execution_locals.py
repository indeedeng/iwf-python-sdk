import inspect
import time
import unittest

from iwf.rpc import rpc
from iwf.client import Client
from iwf.command_request import CommandRequest
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.persistence import Persistence
from iwf.persistence_schema import PersistenceField, PersistenceSchema
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_options import WorkflowOptions
from iwf.workflow_state import T, WorkflowState

PERSISTENCE_LOCAL_KEY = "persistence-test-key"
PERSISTENCE_LOCAL_VALUE = "persistence-test-value"
PERSISTENCE_DATA_ATTRIBUTE_KEY = "persistence-data-attribute-key"


class PersistenceStateExecutionLocalRWState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ):
        persistence.set_state_execution_local(
            PERSISTENCE_LOCAL_KEY, PERSISTENCE_LOCAL_VALUE
        )
        return CommandRequest.empty()

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ):
        value = persistence.get_state_execution_local(PERSISTENCE_LOCAL_KEY)
        persistence.set_data_attribute(PERSISTENCE_DATA_ATTRIBUTE_KEY, value)
        return StateDecision.graceful_complete_workflow()


class PersistenceStateExecutionLocalWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(PersistenceStateExecutionLocalRWState())

    def get_persistence_schema(self) -> PersistenceSchema:
        return PersistenceSchema.create(
            PersistenceField.data_attribute_def(PERSISTENCE_DATA_ATTRIBUTE_KEY, str)
        )

    @rpc()
    def test_persistence_read(self, persistence: Persistence):
        return persistence.get_data_attribute(PERSISTENCE_DATA_ATTRIBUTE_KEY)


class TestPersistenceExecutionLocalRead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = PersistenceStateExecutionLocalWorkflow()
        registry.add_workflow(wf)
        cls.client = Client(registry)

    def test_persistence_execution_local_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        start_options = WorkflowOptions()
        self.client.start_workflow(
            PersistenceStateExecutionLocalWorkflow, wf_id, 200, None, start_options
        )
        self.client.wait_for_workflow_completion(wf_id, None)
        res = self.client.invoke_rpc(
            wf_id, PersistenceStateExecutionLocalWorkflow.test_persistence_read
        )
        assert res == PERSISTENCE_LOCAL_VALUE
