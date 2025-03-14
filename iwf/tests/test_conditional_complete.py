import inspect
import time
import unittest

from iwf.client import Client
from iwf.command_request import (
    CommandRequest,
    InternalChannelCommand,
    SignalChannelCommand,
)
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

test_signal_channel = "test-1"
test_internal_channel = "test-2"

da_counter = "counter"


class WaitState(WorkflowState[bool]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        use_signal: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        if use_signal:
            return CommandRequest.for_all_command_completed(
                SignalChannelCommand.by_name(test_signal_channel),
            )
        else:
            return CommandRequest.for_all_command_completed(
                InternalChannelCommand.by_name(test_internal_channel),
            )

    def execute(
        self,
        ctx: WorkflowContext,
        use_signal: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        counter = persistence.get_data_attribute(da_counter)
        if counter is None:
            counter = 0
        counter += 1
        persistence.set_data_attribute(da_counter, counter)

        if ctx.state_execution_id == "WaitState-1":
            # wait for 3 seconds so that the channel can have a new message
            time.sleep(3)
        if use_signal:
            return StateDecision.force_complete_if_signal_channel_empty_or_else(
                test_signal_channel, counter, WaitState, use_signal
            )
        else:
            return StateDecision.force_complete_if_internal_channel_empty_or_else(
                test_internal_channel, counter, WaitState, use_signal
            )


class ConditionalCompleteWorkflow(ObjectWorkflow):
    def get_communication_schema(self) -> CommunicationSchema:
        return CommunicationSchema.create(
            CommunicationMethod.signal_channel_def(test_signal_channel, int),
            CommunicationMethod.internal_channel_def(test_internal_channel, int),
        )

    def get_persistence_schema(self) -> PersistenceSchema:
        return PersistenceSchema.create(
            PersistenceField.data_attribute_def(da_counter, int),
        )

    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(WaitState())

    @rpc()
    def test_rpc_publish_channel(self, com: Communication):
        com.publish_to_internal_channel(test_internal_channel, 0)


class TestConditionalComplete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = ConditionalCompleteWorkflow()
        registry.add_workflow(wf)

    def test_internal_channel_conditional_complete(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.do_test_conditional_workflow(wf_id, False)

    def test_signal_channel_conditional_complete(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.do_test_conditional_workflow(wf_id, True)

    def do_test_conditional_workflow(self, wf_id: str, use_signal: bool):
        self.client = Client(registry)

        self.client.start_workflow(ConditionalCompleteWorkflow, wf_id, 10, use_signal)

        for x in range(3):
            if use_signal:
                self.client.signal_workflow(wf_id, test_signal_channel, 123)
            else:
                self.client.invoke_rpc(
                    wf_id, ConditionalCompleteWorkflow.test_rpc_publish_channel
                )
            if x == 0:
                # wait for a second so that the workflow is in execute state
                time.sleep(1)

        res = self.client.get_simple_workflow_result_with_wait(wf_id)
        assert res == 3
