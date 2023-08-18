import inspect
import time
from threading import Thread

from iwf.client import Client
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision, graceful_complete_workflow
from iwf.state_schema import StateSchema, starting_state
from iwf.tests.worker_server import registry, workflow_worker
from iwf.utils.iwf_typing import none_type
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import WorkflowState, T


class HelloState(WorkflowState[None]):
    def get_input_type(self) -> type[T]:
        return none_type()

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return graceful_complete_workflow()


class HelloWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema([starting_state(HelloState())])


def test_start_workflow():
    hello_wf = HelloWorkflow()
    registry.add_workflow(hello_wf)

    client = Client(registry)
    wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

    thread = Thread(target=workflow_worker.run, args=("127.0.0.1", 8802))
    thread.start()

    client.start_workflow(HelloWorkflow, wf_id, 100)
    client.get_simple_workflow_result_with_wait(wf_id)
    time.sleep(60)
    thread._stop()
