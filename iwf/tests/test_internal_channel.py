import inspect
import time
import unittest

from iwf.client import Client
from iwf.command_request import CommandRequest, InternalChannelCommand
from iwf.command_results import CommandResults, InternalChannelCommandResult
from iwf.communication import Communication
from iwf.communication_schema import CommunicationMethod, CommunicationSchema
from iwf.iwf_api.models import ChannelRequestStatus
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState

test_channel_name1 = "test-internal-channel-1"
test_channel_name2 = "test-internal-channel-2"

test_channel_name3 = "test-internal-channel-3"
test_channel_name4 = "test-internal-channel-4"

test_channel_name_prefix = "test-internal-channel-prefix-"


class InitState(WorkflowState[None]):
    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return StateDecision.multi_next_states(
            WaitAnyWithPublishState, WaitAllThenPublishState
        )


class WaitAnyWithPublishState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        communication.publish_to_internal_channel(test_channel_name3, 123)
        communication.publish_to_internal_channel(test_channel_name4, "str-value")
        communication.publish_to_internal_channel(
            test_channel_name_prefix + "abc", "str-value-for-prefix"
        )
        return CommandRequest.for_any_command_completed(
            InternalChannelCommand.by_name(test_channel_name1),
            InternalChannelCommand.by_name(test_channel_name2),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        assert len(command_results.internal_channel_commands) == 2
        assert command_results.internal_channel_commands[
            0
        ] == InternalChannelCommandResult(
            channel_name=test_channel_name1,
            command_id="",
            status=ChannelRequestStatus.WAITING,
            value=None,
        )
        assert command_results.internal_channel_commands[
            1
        ] == InternalChannelCommandResult(
            channel_name=test_channel_name2,
            command_id="",
            status=ChannelRequestStatus.RECEIVED,
            value=None,
        )
        return StateDecision.graceful_complete_workflow()


class WaitAllThenPublishState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            InternalChannelCommand.by_name(test_channel_name3),
            InternalChannelCommand.by_name(test_channel_name4),
            InternalChannelCommand.by_name(test_channel_name_prefix + "abc"),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        communication.publish_to_internal_channel(test_channel_name2, None)
        return StateDecision.dead_end


class InternalChannelWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(
            InitState(), WaitAnyWithPublishState(), WaitAllThenPublishState()
        )

    def get_communication_schema(self) -> CommunicationSchema:
        return CommunicationSchema.create(
            CommunicationMethod.internal_channel_def(test_channel_name1, int),
            CommunicationMethod.internal_channel_def(test_channel_name2, None),
            CommunicationMethod.internal_channel_def(test_channel_name3, int),
            CommunicationMethod.internal_channel_def(test_channel_name4, str),
            CommunicationMethod.internal_channel_def_by_prefix(
                test_channel_name_prefix, str
            ),
        )


wf = InternalChannelWorkflow()
registry.add_workflow(wf)
client = Client(registry)


class TestConditionalComplete(unittest.TestCase):
    def test_internal_channel_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        client.start_workflow(InternalChannelWorkflow, wf_id, 100, None)
        client.get_simple_workflow_result_with_wait(wf_id, None)
