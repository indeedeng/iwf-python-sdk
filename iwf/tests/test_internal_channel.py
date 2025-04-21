import inspect
import time
import unittest

from iwf.client import Client
from iwf.tests.worker_server import registry
from iwf.tests.workflows.internal_channel_workflow import InternalChannelWorkflow


class TestConditionalComplete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client(registry)

    def test_internal_channel_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        self.client.start_workflow(InternalChannelWorkflow, wf_id, 100, None)
        self.client.wait_for_workflow_completion(wf_id, None)
