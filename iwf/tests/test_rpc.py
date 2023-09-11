import inspect
import time
import unittest

from iwf.client import Client
from iwf.communication import Communication
from iwf.persistence import Persistence
from iwf.rpc import rpc
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext


class RPCWorkflow(ObjectWorkflow):
    @rpc(timeout_seconds=100)
    def test_simple_rpc(self):
        return 123

    @rpc(timeout_seconds=100)
    def test_rpc(
        self,
        context: WorkflowContext,
        input: int,
        persistence: Persistence,
        communication: Communication,
    ):
        return input


class TestRPCs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = RPCWorkflow()
        registry.add_workflow(wf)
        cls.client = Client(registry)

    def test_simple_rpc(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.client.start_workflow(RPCWorkflow, wf_id, 10)
        output = self.client.invoke_rpc(wf_id, RPCWorkflow.test_simple_rpc)
        assert output == 123
        wf = RPCWorkflow()
        output = self.client.invoke_rpc(wf_id, wf.test_simple_rpc)
        assert output == 123
