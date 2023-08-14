from iwf_api.models import WorkflowStopType
from pydantic.main import BaseModel


class StopWorkflowOptions(BaseModel):
    workflow_stop_type: WorkflowStopType
    reason: str
