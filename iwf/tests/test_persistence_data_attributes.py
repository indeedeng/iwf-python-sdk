import inspect
import time
import unittest

from iwf.client import Client
from iwf.tests.worker_server import registry
from iwf.tests.workflows.persistence_data_attributes_workflow import (
    PersistenceDataAttributesWorkflow,
    initial_da_1,
    initial_da_2,
    initial_da_value_2,
    initial_da_value_1,
    test_da_set_key,
    test_da_set_value,
    expected_final_das,
)
from iwf.workflow_options import WorkflowOptions


class TestPersistenceDataAttributes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
