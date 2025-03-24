from dataclasses import dataclass
from iwf.iwf_api.models.workflow_status import WorkflowStatus


@dataclass
class WorkflowInfo:
    workflow_status: WorkflowStatus
