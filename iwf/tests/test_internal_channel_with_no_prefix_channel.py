import inspect
import time
import unittest

from iwf.client import Client
from iwf.command_request import CommandRequest, InternalChannelCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.communication_schema import CommunicationMethod, CommunicationSchema
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState

internal_channel_name = "internal-channel-1"

test_non_prefix_channel_name = "test-channel-"
test_non_prefix_channel_name_with_suffix = test_non_prefix_channel_name + "abc"


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
        # Trying to publish to a non-existing channel; this would only work if test_channel_name_non_prefix was defined as a prefix channel
        communication.publish_to_internal_channel(
            test_non_prefix_channel_name_with_suffix, "str-value-for-prefix"
        )
        return CommandRequest.for_any_command_completed(
            InternalChannelCommand.by_name(internal_channel_name),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
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
            InternalChannelCommand.by_name(test_non_prefix_channel_name),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        communication.publish_to_internal_channel(internal_channel_name, None)
        return StateDecision.dead_end


class InternalChannelWorkflowWithNoPrefixChannel(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(
            InitState(), WaitAnyWithPublishState(), WaitAllThenPublishState()
        )

    def get_communication_schema(self) -> CommunicationSchema:
        return CommunicationSchema.create(
            CommunicationMethod.internal_channel_def(internal_channel_name, None),
            # Defining a standard channel (non-prefix) to make sure messages to the channel with a suffix added will not be accepted
            CommunicationMethod.internal_channel_def(test_non_prefix_channel_name, str),
        )


wf = InternalChannelWorkflowWithNoPrefixChannel()
registry.add_workflow(wf)
client = Client(registry)


class TestInternalChannelWithNoPrefix(unittest.TestCase):
    def test_internal_channel_workflow_with_no_prefix_channel(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        client.start_workflow(
            InternalChannelWorkflowWithNoPrefixChannel, wf_id, 5, None
        )

        with self.assertRaises(Exception) as context:
            client.wait_for_workflow_completion(wf_id, None)

        self.assertIn("FAILED", context.exception.workflow_status)
        self.assertIn(
            f"WorkerExecutionError: InternalChannel channel_name is not defined {test_non_prefix_channel_name_with_suffix}",
            context.exception.error_message,
        )
