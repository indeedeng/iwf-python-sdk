import inspect
import time
import unittest

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

initial_da_1 = "initial_da_1"
initial_da_value_1 = "value_1"
initial_da_2 = "initial_da_2"
initial_da_value_2 = "value_2"

test_da_1 = "test_da_1"
test_da_2 = "test_da_2"

final_test_da_value_1 = "1234"
final_test_da_value_2 = 1234
final_initial_da_value_1 = initial_da_value_1
final_initial_da_value_2 = "no-more-init"

test_da_prefix = "test-da-prefix"
test_da_prefix_key_1 = "test-da-prefix-1"
test_da_prefix_key_2 = "test-da-prefix-2"
test_da_prefix_value_1 = "test-da-value-1"
test_da_prefix_value_2 = "test-da-value-2"
test_da_set_key = "test_da_set_key"
test_da_set_value = "test_da_set_value"

expected_final_das = {
    initial_da_1: initial_da_value_1,
    initial_da_2: final_initial_da_value_2,
    test_da_1: final_test_da_value_1,
    test_da_2: final_test_da_value_2,
    test_da_prefix_key_1: test_da_prefix_value_1,
    test_da_prefix_key_2: test_da_prefix_value_2,
    test_da_set_key: test_da_set_value,
}


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

        persistence.set_data_attribute(test_da_1, final_test_da_value_1)
        persistence.set_data_attribute(test_da_2, final_test_da_value_2)
        persistence.set_data_attribute(initial_da_2, final_initial_da_value_2)
        persistence.set_data_attribute(test_da_prefix_key_1, test_da_prefix_value_1)
        persistence.set_data_attribute(test_da_prefix_key_2, test_da_prefix_value_2)
        return StateDecision.graceful_complete_workflow()


class PersistenceDataAttributesWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(DataAttributeRWState())

    def get_persistence_schema(self) -> PersistenceSchema:
        return PersistenceSchema.create(
            PersistenceField.data_attribute_def(initial_da_1, str),
            PersistenceField.data_attribute_def(initial_da_2, str),
            PersistenceField.data_attribute_def(test_da_1, str),
            PersistenceField.data_attribute_def(test_da_2, int),
            PersistenceField.data_attribute_prefix_def(test_da_prefix, str),
            PersistenceField.data_attribute_def(test_da_set_key, str),
        )


class TestPersistenceDataAttributes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = PersistenceDataAttributesWorkflow()
        registry.add_workflow(wf)
        cls.client = Client(registry)

    def test_persistence_data_attributes_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        start_options = WorkflowOptions(
            initial_data_attributes={
                initial_da_1: initial_da_value_1,
                initial_da_2: initial_da_value_2,
            },
        )

        wf_run_id = self.client.start_workflow(
            PersistenceDataAttributesWorkflow, wf_id, 100, None, start_options
        )
        self.client.set_workflow_data_attributes(
            PersistenceDataAttributesWorkflow,
            wf_id,
            wf_run_id,
            {
                test_da_set_key: test_da_set_value,
            },
        )
        self.client.wait_for_workflow_completion(wf_id, None)

        all_data_attributes = self.client.get_all_workflow_data_attributes(
            PersistenceDataAttributesWorkflow, wf_id, wf_run_id
        )
        for k, v in expected_final_das.items():
            assert k in all_data_attributes
            assert all_data_attributes[k] == v
