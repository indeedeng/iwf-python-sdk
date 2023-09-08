import inspect
import time

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
from iwf.workflow_state import T, WorkflowState

test_da_1 = "test_da_1"
test_da_2 = "test_da_2"


class DataAttributeRWState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        persistence.set_data_attribute(test_da_1, "123")
        persistence.set_data_attribute(test_da_2, 123)

        return CommandRequest.empty()

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        da1 = persistence.get_data_attribute(test_da_1)
        da2 = persistence.get_data_attribute(test_da_2)
        assert da1 == "123"
        assert da2 == 123

        persistence.set_data_attribute(test_da_1, "1234")
        persistence.set_data_attribute(test_da_2, 1234)
        return StateDecision.graceful_complete_workflow()


class PersistenceWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(DataAttributeRWState())

    def get_persistence_schema(self) -> PersistenceSchema:
        return PersistenceSchema.create(
            PersistenceField.data_attribute_def(test_da_1, str),
            PersistenceField.data_attribute_def(test_da_2, int),
        )


wf = PersistenceWorkflow()
registry.add_workflow(wf)
client = Client(registry)


def test_persistence_workflow():
    wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

    client.start_workflow(PersistenceWorkflow, wf_id, 100, None)
    client.get_simple_workflow_result_with_wait(wf_id, None)
    # TODO use RPC to get the final result of the persistence updated in execute API
