from typing import Optional

from iwf.command_request import CommandRequest, InternalChannelCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.communication_schema import CommunicationMethod, CommunicationSchema
from iwf.iwf_api.models.search_attribute_value_type import SearchAttributeValueType
from iwf.persistence import Persistence
from iwf.persistence_options import PersistenceOptions
from iwf.persistence_schema import PersistenceField, PersistenceSchema
from iwf.rpc import rpc
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import WorkflowState


"""
NOTE: This workflow and its tests were translated from iwf-java-sdk, but currently, there is a
discrepency between the sdks in their handling of empty graceful complete workflow
messages. These tests will not pass, so they are curretly being skipped. They were added
here for posterity.
"""


INTERNAL_CHANNEL_NAME = "test-channel-1"
TEST_DATA_OBJECT_KEY = "data-obj-1"
TEST_SEARCH_ATTRIBUTE_KEY = "CustomKeywordField"
TEST_SEARCH_ATTRIBUTE_INT = "CustomIntField"
RPC_INPUT = "rpc-input"
RPC_OUTPUT = 100
TEST_STR = "test-str"
TEST_DELAY = 0.1


class JavaDuplicateRpcMemoWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(
            RpcMemoWorkflowState1(), RpcMemoWorkflowState2()
        )

    def get_persistence_schema(self) -> PersistenceSchema:
        return PersistenceSchema.create(
            PersistenceField.data_attribute_def(TEST_DATA_OBJECT_KEY, str),
            PersistenceField.search_attribute_def(
                TEST_SEARCH_ATTRIBUTE_INT, SearchAttributeValueType.INT
            ),
            PersistenceField.search_attribute_def(
                TEST_SEARCH_ATTRIBUTE_KEY, SearchAttributeValueType.KEYWORD
            ),
        )

    def get_communication_schema(self) -> CommunicationSchema:
        return CommunicationSchema.create(
            CommunicationMethod.internal_channel_def(INTERNAL_CHANNEL_NAME, None)
        )

    def get_persistence_options(self) -> PersistenceOptions:
        return PersistenceOptions(enable_caching=True)

    @rpc()
    def test_rpc_func1(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ) -> int:
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")

        persistence.set_data_attribute(TEST_DATA_OBJECT_KEY, None)
        persistence.set_data_attribute(TEST_DATA_OBJECT_KEY, input)
        persistence.set_search_attribute_keyword(TEST_SEARCH_ATTRIBUTE_KEY, input)
        persistence.set_search_attribute_int64(TEST_SEARCH_ATTRIBUTE_INT, RPC_OUTPUT)
        communication.publish_to_internal_channel(INTERNAL_CHANNEL_NAME, None)
        communication.trigger_state_execution(RpcMemoWorkflowState2)
        return RPC_OUTPUT

    @rpc()
    def test_rpc_func0(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ) -> int:
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")

        persistence.set_data_attribute(TEST_DATA_OBJECT_KEY, TEST_STR)
        persistence.set_search_attribute_keyword(TEST_SEARCH_ATTRIBUTE_KEY, TEST_STR)
        persistence.set_search_attribute_int64(TEST_SEARCH_ATTRIBUTE_INT, RPC_OUTPUT)
        communication.publish_to_internal_channel(INTERNAL_CHANNEL_NAME, None)
        communication.trigger_state_execution(RpcMemoWorkflowState2)
        return RPC_OUTPUT

    @rpc()
    def test_rpc_proc1(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ):
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")

        persistence.set_data_attribute(TEST_DATA_OBJECT_KEY, input)
        persistence.set_search_attribute_keyword(TEST_SEARCH_ATTRIBUTE_KEY, input)
        persistence.set_search_attribute_int64(TEST_SEARCH_ATTRIBUTE_INT, RPC_OUTPUT)
        communication.publish_to_internal_channel(INTERNAL_CHANNEL_NAME, None)
        communication.trigger_state_execution(RpcMemoWorkflowState2)

    @rpc()
    def test_rpc_proc0(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ):
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")

        persistence.set_data_attribute(TEST_DATA_OBJECT_KEY, TEST_STR)
        persistence.set_search_attribute_keyword(TEST_SEARCH_ATTRIBUTE_KEY, TEST_STR)
        persistence.set_search_attribute_int64(TEST_SEARCH_ATTRIBUTE_INT, RPC_OUTPUT)
        communication.publish_to_internal_channel(INTERNAL_CHANNEL_NAME, None)
        communication.trigger_state_execution(RpcMemoWorkflowState2)

    @rpc()
    def test_rpc_func1_readonly(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ) -> int:
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")
        return RPC_OUTPUT

    @rpc()
    def test_rpc_set_data_attribute(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ):
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")
        persistence.set_data_attribute(TEST_DATA_OBJECT_KEY, input)

    @rpc()
    def test_rpc_get_data_attribute(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ) -> str:
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")
        return persistence.get_data_attribute(TEST_DATA_OBJECT_KEY)

    @rpc(bypass_caching_for_strong_consistency=True)
    def test_rpc_get_data_attribute_strong_consistency(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ) -> str:
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")
        return persistence.get_data_attribute(TEST_DATA_OBJECT_KEY)

    @rpc()
    def test_rpc_set_keyword(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ):
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")
        persistence.set_search_attribute_keyword(TEST_SEARCH_ATTRIBUTE_KEY, input)

    @rpc(bypass_caching_for_strong_consistency=True)
    def test_rpc_get_keyword_strong_consistency(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ) -> Optional[str]:
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")
        return persistence.get_search_attribute_keyword(TEST_SEARCH_ATTRIBUTE_KEY)

    @rpc()
    def test_rpc_get_keyword(
        self,
        ctx: WorkflowContext,
        input: str,
        persistence: Persistence,
        communication: Communication,
    ) -> Optional[str]:
        if not ctx.workflow_id or not ctx.workflow_run_id:
            raise RuntimeError("invalid context")
        return persistence.get_search_attribute_keyword(TEST_SEARCH_ATTRIBUTE_KEY)


class RpcMemoWorkflowState1(WorkflowState[int]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: int,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_any_command_completed(
            InternalChannelCommand.by_name(INTERNAL_CHANNEL_NAME)
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: int,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return StateDecision.single_next_state(RpcMemoWorkflowState2, 0)


class RpcMemoWorkflowState2(WorkflowState[int]):
    _counter: int = 0

    def wait_until(
        self,
        ctx: WorkflowContext,
        input: int,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.empty()

    def execute(
        self,
        ctx: WorkflowContext,
        input: int,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        self._counter += 1
        if self._counter == 2:
            return StateDecision.graceful_complete_workflow(self._counter)
        else:
            return StateDecision.graceful_complete_workflow()

    @classmethod
    def reset_counter(cls) -> int:
        old = cls._counter
        cls._counter = 0
        return old
