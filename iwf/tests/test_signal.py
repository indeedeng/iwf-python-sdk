import inspect
import time
import unittest

from iwf_api.models import ChannelRequestStatus

from iwf.client import Client
from iwf.command_request import (
    CommandRequest,
    SignalChannelCommand,
)
from iwf.command_results import CommandResults, SignalChannelCommandResult
from iwf.communication import Communication
from iwf.communication_schema import CommunicationMethod, CommunicationSchema
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState

test_channel_int = "test-int"
test_channel_none = "test-none"
test_channel_str = "test-str"


class WaitState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            SignalChannelCommand.by_name(test_channel_int),
            SignalChannelCommand.by_name(test_channel_none),
            SignalChannelCommand.by_name(test_channel_str),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        assert len(command_results.signal_channel_commands) == 3
        sig1 = command_results.signal_channel_commands[0]
        sig2 = command_results.signal_channel_commands[1]
        sig3 = command_results.signal_channel_commands[2]
        assert sig1 == SignalChannelCommandResult(
            test_channel_int, 123, ChannelRequestStatus.RECEIVED, ""
        )
        assert sig2 == SignalChannelCommandResult(
            test_channel_none, None, ChannelRequestStatus.RECEIVED, ""
        )
        assert sig3 == SignalChannelCommandResult(
            test_channel_str, "abc", ChannelRequestStatus.RECEIVED, ""
        )
        return StateDecision.graceful_complete_workflow(sig3.value)


class WaitSignalWorkflow(ObjectWorkflow):
    def get_communication_schema(self) -> CommunicationSchema:
        return CommunicationSchema.create(
            CommunicationMethod.signal_channel_def(test_channel_int, int),
            CommunicationMethod.signal_channel_def(test_channel_none, type(None)),
            CommunicationMethod.signal_channel_def(test_channel_str, str),
        )

    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(WaitState())


class TestSignal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = WaitSignalWorkflow()
        registry.add_workflow(wf)
        cls.client = Client(registry)

    def test_signal(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.client.start_workflow(WaitSignalWorkflow, wf_id, 1)
        self.client.signal_workflow(wf_id, test_channel_int, 123)
        self.client.signal_workflow(wf_id, test_channel_str, "abc")
        self.client.signal_workflow(wf_id, test_channel_none)
        res = self.client.get_simple_workflow_result_with_wait(wf_id)
        assert res == "abc"
