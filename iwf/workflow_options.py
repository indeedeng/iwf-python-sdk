from dataclasses import dataclass
from typing import Optional

from iwf.iwf_api.models import IDReusePolicy, WorkflowRetryPolicy


@dataclass
class WorkflowOptions:
    workflow_id_reuse_policy: Optional[IDReusePolicy] = None
    workflow_cron_schedule: Optional[str] = None
    workflow_start_delay_seconds: Optional[int] = None
    workflow_retry_policy: Optional[WorkflowRetryPolicy] = None
    # initial_search_attributes: Optional[dict[str, Any]] = None
