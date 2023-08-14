from dataclasses import dataclass

from workflow_state import WorkflowState


@dataclass
class StateDef:
    state: WorkflowState
    can_start_workflow: bool
