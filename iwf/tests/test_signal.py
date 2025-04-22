import inspect
import time
import unittest

from iwf.client import Client
from iwf.tests.worker_server import registry
from iwf.tests.workflows.wait_signal_workflow import (
    WaitSignalWorkflow,
    test_channel_int,
    test_channel_str,
    test_channel_none,
    test_channel1,
    test_idle_channel_none,
)


class TestSignal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client(registry)

    def test_signal(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.client.start_workflow(WaitSignalWorkflow, wf_id, 10)
        self.client.signal_workflow(wf_id, test_channel_int, 123)
        self.client.signal_workflow(wf_id, test_channel_str, "abc")
        self.client.signal_workflow(wf_id, test_channel_none)

        self.client.signal_workflow(wf_id, test_channel1)
        res = self.client.wait_for_workflow_completion(wf_id, str)
        assert res == "abc"

    def test_signal_channel_size(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.client.start_workflow(WaitSignalWorkflow, wf_id, 1)
        self.client.signal_workflow(wf_id, test_idle_channel_none)
        self.client.signal_workflow(wf_id, test_idle_channel_none)
        self.client.signal_workflow(wf_id, test_idle_channel_none)
        res = self.client.invoke_rpc(
            wf_id, WaitSignalWorkflow.get_idle_signal_channel_size
        )
        assert res == 3
