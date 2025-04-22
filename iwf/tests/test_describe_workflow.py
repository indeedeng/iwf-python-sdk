import inspect
import time
import unittest

from iwf.client import Client
from iwf.errors import WorkflowNotExistsError
from iwf.iwf_api.models import WorkflowStatus
from iwf.tests.workflows.describe_workflow import DescribeWorkflow
from iwf.tests.worker_server import registry


class TestDescribeWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client(registry)

    def test_describe_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        self.client.start_workflow(DescribeWorkflow, wf_id, 100)
        workflow_info = self.client.describe_workflow(wf_id)
        assert workflow_info.workflow_status == WorkflowStatus.RUNNING

        # Stop the workflow
        self.client.stop_workflow(wf_id)

    def test_describe_workflow_when_workflow_not_exists(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        with self.assertRaises(WorkflowNotExistsError):
            self.client.describe_workflow(wf_id)
