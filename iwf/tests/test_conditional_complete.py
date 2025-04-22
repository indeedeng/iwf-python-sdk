import inspect
import time
import unittest

from iwf.client import Client
from iwf.tests.worker_server import registry
from iwf.tests.workflows.conditional_complete_workflow import (
    ConditionalCompleteWorkflow,
    test_signal_channel,
)


class TestConditionalComplete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client(registry)

    def test_internal_channel_conditional_complete(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        do_test_conditional_workflow(self.client, wf_id, False)

    def test_signal_channel_conditional_complete(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        do_test_conditional_workflow(self.client, wf_id, True)


def do_test_conditional_workflow(client: Client, wf_id: str, use_signal: bool):
    client.start_workflow(ConditionalCompleteWorkflow, wf_id, 10, use_signal)

    for x in range(3):
        if use_signal:
            client.signal_workflow(wf_id, test_signal_channel, 123)
        else:
            client.invoke_rpc(
                wf_id, ConditionalCompleteWorkflow.test_rpc_publish_channel
            )
        if x == 0:
            # wait for a second so that the workflow is in execute state
            time.sleep(1)

    res = client.wait_for_workflow_completion(wf_id)
    assert res == 3
