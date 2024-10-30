import inspect
import time

from iwf.client import Client
from iwf.command_request import CommandRequest, TimerCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState


class WaitState(WorkflowState[int]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: int,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(input * 3600),
            TimerCommand.by_seconds(input),
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


class TimerWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(WaitState())


wf = TimerWorkflow()
registry.add_workflow(wf)
client = Client(registry)


def test_timer_workflow():
    wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

    client.start_workflow(TimerWorkflow, wf_id, 100, 5)
    time.sleep(1)
    client.skip_timer_at_command_index(wf_id, WaitState)
    start_ms = time.time_ns() / 1000000
    client.get_simple_workflow_result_with_wait(wf_id, None)
    elapsed_ms = time.time_ns() / 1000000 - start_ms
    assert 3000 <= elapsed_ms <= 6000, f"expected 5000 ms timer, actual is {elapsed_ms}"
