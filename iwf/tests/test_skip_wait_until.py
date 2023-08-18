from iwf.command_request import CommandRequest
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState, should_skip_wait_until


class DirectStateSkip(WorkflowState[None]):
    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        raise NotImplementedError


class DirectStateNotSkip(WorkflowState[int]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: int,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        raise NotImplementedError

    def execute(
        self,
        ctx: WorkflowContext,
        input: int,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        raise NotImplementedError


class IndirectStateSkip(DirectStateSkip):
    pass


class IndirectStateNotSkip(DirectStateSkip):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        raise NotImplementedError


def test_should_skip_wait_until() -> None:
    direct_skip = DirectStateSkip()
    direct_not_skip = DirectStateNotSkip()
    indirect_skip = IndirectStateSkip()
    indirect_not_skip = IndirectStateNotSkip()

    assert should_skip_wait_until(direct_skip)
    assert should_skip_wait_until(indirect_skip)

    assert not should_skip_wait_until(direct_not_skip)
    assert not should_skip_wait_until(indirect_not_skip)
