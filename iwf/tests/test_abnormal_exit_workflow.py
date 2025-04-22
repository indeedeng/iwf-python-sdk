import inspect
import time
import unittest

from iwf.client import Client
from iwf.errors import WorkflowFailed
from iwf.iwf_api.models.id_reuse_policy import IDReusePolicy
from iwf.tests.worker_server import registry
from iwf.tests.workflows.abnormal_exit_workflow import AbnormalExitWorkflow
from iwf.tests.workflows.basic_workflow import BasicWorkflow
from iwf.workflow_options import WorkflowOptions


class TestAbnormalWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client(registry)

    def test_abnormal_exit_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        start_options = WorkflowOptions(
            workflow_id_reuse_policy=IDReusePolicy.ALLOW_IF_PREVIOUS_EXITS_ABNORMALLY
        )

        self.client.start_workflow(
            AbnormalExitWorkflow, wf_id, 100, "input", start_options
        )
        with self.assertRaises(WorkflowFailed):
            self.client.wait_for_workflow_completion(wf_id, str)

        # Starting a workflow with the same ID should be allowed since the previous failed abnormally
        self.client.start_workflow(BasicWorkflow, wf_id, 100, "input", start_options)
        res = self.client.wait_for_workflow_completion(wf_id, str)
        assert res == "done"
