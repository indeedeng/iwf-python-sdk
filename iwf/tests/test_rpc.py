import inspect
import time
import unittest
from dataclasses import dataclass

from iwf.client import Client
from iwf.command_request import CommandRequest, InternalChannelCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.communication_schema import CommunicationMethod, CommunicationSchema
from iwf.persistence import Persistence
from iwf.persistence_schema import PersistenceField, PersistenceSchema
from iwf.rpc import rpc
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState

test_data_attribute = "test-1"
channel_name = "test-2"
idle_channel_name = "test-3"


@dataclass
class Mydata:
    strdata: str
    intdata: int


class WaitState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            InternalChannelCommand.by_name(channel_name)
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return StateDecision.single_next_state(EndState)


class EndState(WorkflowState[None]):
    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return StateDecision.graceful_complete_workflow("done")


class RPCWorkflow(ObjectWorkflow):
    def get_persistence_schema(self) -> PersistenceSchema:
        return PersistenceSchema.create(
            PersistenceField.data_attribute_def(test_data_attribute, int)
        )

    def get_communication_schema(self) -> CommunicationSchema:
        return CommunicationSchema.create(
            CommunicationMethod.internal_channel_def(channel_name, type(None)),
            CommunicationMethod.internal_channel_def(idle_channel_name, str),
        )

    def get_workflow_states(self) -> StateSchema:
        return StateSchema.no_starting_state(WaitState(), EndState())

    @rpc(timeout_seconds=100)
    def test_simple_rpc(self):
        return 123

    @rpc()
    def test_rpc_persistence_write(
        self,
        input: int,
        persistence: Persistence,
    ):
        persistence.set_data_attribute(test_data_attribute, input)

    @rpc()
    def test_rpc_persistence_read(self, pers: Persistence):
        return pers.get_data_attribute(test_data_attribute)

    @rpc()
    def test_rpc_trigger_state(self, pers: Persistence, com: Communication, i: int):
        pers.set_data_attribute(test_data_attribute, i)
        com.trigger_state_execution(WaitState)

    @rpc()
    def test_rpc_publish_channel(self, com: Communication):
        com.publish_to_internal_channel(channel_name)

    @rpc()
    def test_rpc_publish_to_idle_channel(self, com: Communication, data: str):
        com.publish_to_internal_channel(idle_channel_name, data)
        return com.get_internal_channel_size(idle_channel_name)

    @rpc()
    def test_rpc_input_type(self, input: Mydata) -> Mydata:
        if input.intdata != 100 or input.strdata != "test":
            raise Exception("input type test failed")
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

        input = Mydata("test", 100)
        output = self.client.invoke_rpc(
            wf_id, RPCWorkflow.test_rpc_input_type, input, Mydata
        )
        assert output == input

        output = self.client.invoke_rpc(wf_id, RPCWorkflow.test_simple_rpc)
        assert output == 123
        wf = RPCWorkflow()
        output = self.client.invoke_rpc(wf_id, wf.test_simple_rpc)
        assert output == 123

    def test_complicated_rpc(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.client.start_workflow(RPCWorkflow, wf_id, 10)
        self.client.invoke_rpc(wf_id, RPCWorkflow.test_rpc_persistence_write, 100)
        res = self.client.invoke_rpc(wf_id, RPCWorkflow.test_rpc_persistence_read)
        assert res == 100
        self.client.invoke_rpc(wf_id, RPCWorkflow.test_rpc_trigger_state, 200)
        res = self.client.invoke_rpc(wf_id, RPCWorkflow.test_rpc_persistence_read)
        assert res == 200

        res1 = self.client.invoke_rpc(
            wf_id, RPCWorkflow.test_rpc_publish_to_idle_channel, "input-1"
        )
        # Channel Size should be 1
        assert res1 == 1

        res2 = self.client.invoke_rpc(
            wf_id, RPCWorkflow.test_rpc_publish_to_idle_channel, "input-2"
        )
        # Channel Size should be 2
        assert res2 == 2

        self.client.invoke_rpc(wf_id, RPCWorkflow.test_rpc_publish_channel)
        result = self.client.get_simple_workflow_result_with_wait(wf_id, str)
        assert result == "done"
