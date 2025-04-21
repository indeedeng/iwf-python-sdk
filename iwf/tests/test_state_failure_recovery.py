import inspect
import time
import unittest

from iwf.client import Client
from iwf.tests.worker_server import registry
from iwf.tests.workflows.recovery_workflow import RecoveryWorkflow


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client(registry)

    def test_workflow_recovery(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.client.start_workflow(RecoveryWorkflow, wf_id, 10)
        result = self.client.wait_for_workflow_completion(wf_id, str)
        assert result == "done"
