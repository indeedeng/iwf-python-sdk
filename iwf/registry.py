from iwf.errors import WorkflowDefinitionError
from iwf.state_def import StateDef
from iwf.workflow import ObjectWorkflow, get_workflow_type
from iwf.workflow_state import get_state_id


class Registry:
    def __init__(self):
        self._workflowStore = {}
        self._startingStateStore = {}
        self._stateStore = {}

    def add_workflow(self, wf: ObjectWorkflow):
        self._register_workflow(wf)
        self._register_workflow_state(wf)

    def add_workflows(self, wfs: [ObjectWorkflow]):
        for wf in wfs:
            self.add_workflow(wf)

    def get_workflow(self, wf_type: str) -> ObjectWorkflow:
        return self._workflowStore[wf_type]

    def get_workflow_starting_state_def(self, wf_type: str) -> StateDef:
        return self._startingStateStore[wf_type]

    def get_workflow_state_defs(self, wf_type: str) -> dict[str, StateDef]:
        return self._stateStore[wf_type]

    def _register_workflow(self, wf):
        wf_type = get_workflow_type(wf)
        if wf_type in self._workflowStore:
            raise WorkflowDefinitionError("workflow type conflict: ", wf_type)
        self._workflowStore[wf_type] = wf

    def _register_workflow_state(self, wf):
        wf_type = get_workflow_type(wf)
        state_map = {}
        starting_state = None
        for state_def in wf.get_workflow_states():
            state_id = get_state_id(state_def.state)
            if state_id in state_map:
                raise WorkflowDefinitionError(
                    "Workflow {} cannot have duplicate stateId {}".format(
                        wf_type, state_id
                    )
                )
            state_map[state_id] = state_def.state
            if state_def.can_start_workflow:
                if starting_state is not None:
                    raise WorkflowDefinitionError(
                        "Workflow {} cannot contain more than one starting state ".format(
                            wf_type
                        )
                    )
                starting_state = state_def.state
            self._stateStore[wf_type] = state_map
            self._startingStateStore[wf_type] = starting_state
