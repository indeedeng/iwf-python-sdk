import inspect
import time
import unittest

from iwf.client import Client
from iwf.workflow_options import WorkflowOptions

from iwf.iwf_api.models import IDReusePolicy
from iwf.tests.worker_server import registry

from iwf.tests.workflows.state_options_override_workflow import (
    StateOptionsOverrideWorkflow,
)


class TestStateOptionsOverrideWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
