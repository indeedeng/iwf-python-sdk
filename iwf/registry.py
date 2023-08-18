from typing import List, Optional

from iwf.errors import WorkflowDefinitionError, InvalidArgumentError
from iwf.workflow import ObjectWorkflow, get_workflow_type
from iwf.workflow_state import get_state_id, WorkflowState


class Registry:
    _workflow_store: dict[str, ObjectWorkflow]
    _starting_state_store: dict[str, WorkflowState]
    _state_store: dict[str, dict[str, WorkflowState]]

    def __init__(self):
        self._workflow_store = dict()
        self._starting_state_store = dict()
        self._state_store = dict()

    def add_workflow(self, wf: ObjectWorkflow):
        self._register_workflow(wf)
        self._register_workflow_state(wf)

    def add_workflows(self, wfs: List[ObjectWorkflow]):
        for wf in wfs:
            self.add_workflow(wf)

    def get_workflow_with_check(self, wf_type: str) -> ObjectWorkflow:
        wf = self._workflow_store.get(wf_type)
        if wf is None:
            raise InvalidArgumentError(f"workflow {wf_type} is not registered")
        return wf

    def get_workflow_starting_state(self, wf_type: str) -> Optional[WorkflowState]:
        return self._starting_state_store.get(wf_type)

    def get_workflow_state_with_check(
        self, wf_type: str, state_id: str
    ) -> WorkflowState:
        states = self._state_store.get(wf_type)
        if states is None:
            raise InvalidArgumentError(f"workflow {wf_type} is not registered")
        state = states.get(state_id)
        if state is None:
            raise InvalidArgumentError(
                f"workflow {wf_type} state {state_id} is not registered"
            )
        return state

    def _register_workflow(self, wf):
        wf_type = get_workflow_type(wf)
        if wf_type in self._workflow_store:
            raise WorkflowDefinitionError("workflow type conflict: ", wf_type)
        self._workflow_store[wf_type] = wf

    def _register_workflow_state(self, wf):
        wf_type = get_workflow_type(wf)
        state_map = {}
        starting_state = None
        for state_def in wf.get_workflow_states().states:
            state_id = get_state_id(state_def.state)
            if state_id in state_map:
                raise WorkflowDefinitionError(
                    f"Workflow {wf_type} cannot have duplicate stateId {state_id}"
                )
            state_map[state_id] = state_def.state
            if state_def.can_start_workflow:
                if starting_state is not None:
                    raise WorkflowDefinitionError(
                        f"Workflow {wf_type} cannot contain more than one starting "
                        f"state"
                    )
                starting_state = state_def.state
            self._state_store[wf_type] = state_map
            self._starting_state_store[wf_type] = starting_state
