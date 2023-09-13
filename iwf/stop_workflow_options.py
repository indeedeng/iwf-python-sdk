from dataclasses import dataclass

from iwf.iwf_api.iwf_api.models import WorkflowStopType


@dataclass
class StopWorkflowOptions:
    workflow_stop_type: WorkflowStopType
    reason: str
