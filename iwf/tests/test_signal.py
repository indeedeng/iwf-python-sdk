import inspect
import time
import unittest

from iwf.client import Client
from iwf.iwf_api.models.timer_result import TimerStatus
from iwf.command_request import (
    CommandRequest,
    SignalChannelCommand,
    TimerCommand,
)
from iwf.command_results import (
    CommandResults,
    SignalChannelCommandResult,
    TimerCommandResult,
)
from iwf.communication import Communication
from iwf.communication_schema import CommunicationMethod, CommunicationSchema
from iwf.iwf_api.models import ChannelRequestStatus
from iwf.persistence import Persistence
from iwf.rpc import rpc
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState

test_channel_int = "test-int"
test_channel_none = "test-none"
test_channel_str = "test-str"
test_idle_channel_none = "test-idle"

test_channel1 = "test-channel1"
test_channel1_id = "test-channel1-id"
test_channel2 = "test-channel2"
test_channel2_id = "test-channel2-id"
test_timer_id = "test-timer-id"


class WaitState1(WorkflowState[None]):
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
        return StateDecision.single_next_state(WaitState2, sig3.value)


class WaitState2(WorkflowState[str]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_any_command_combination_completed(
            [
                [
                    test_channel1_id,
                    test_timer_id,
                ]
            ],
            SignalChannelCommand.by_name(test_channel1, test_channel1_id),
            SignalChannelCommand.by_name(test_channel2, test_channel2_id),
            TimerCommand.by_seconds(1, test_timer_id),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: str,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        assert len(command_results.signal_channel_commands) == 2
        assert (
            len(
                [
                    r
                    for r in command_results.signal_channel_commands
                    if r.status == ChannelRequestStatus.RECEIVED
                ]
            )
            == 1
        )
        sig1 = command_results.signal_channel_commands[0]
        tim1 = command_results.timer_commands[0]
        assert sig1 == SignalChannelCommandResult(
            test_channel1, None, ChannelRequestStatus.RECEIVED, test_channel1_id
        )
        assert tim1 == TimerCommandResult(
            TimerStatus.FIRED,
            test_timer_id,
        )
        return StateDecision.graceful_complete_workflow(input)


class WaitSignalWorkflow(ObjectWorkflow):
    def get_communication_schema(self) -> CommunicationSchema:
        return CommunicationSchema.create(
            CommunicationMethod.signal_channel_def(test_channel_int, int),
            CommunicationMethod.signal_channel_def(test_channel_none, type(None)),
            CommunicationMethod.signal_channel_def(test_channel_str, str),
            CommunicationMethod.signal_channel_def(test_idle_channel_none, type(None)),
            CommunicationMethod.signal_channel_def(test_channel1, type(None)),
            CommunicationMethod.signal_channel_def(test_channel2, type(None)),
        )

    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(WaitState1(), WaitState2())

    @rpc()
    def get_idle_signal_channel_size(self, com: Communication):
        return com.get_signal_channel_size(test_idle_channel_none)


class TestSignal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = WaitSignalWorkflow()
        registry.add_workflow(wf)
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
