from dataclasses import dataclass
from typing import Any

from iwf_api.models import IDReusePolicy, WorkflowRetryPolicy


@dataclass
class WorkflowOptions:
    workflow_id_reuse_policy: IDReusePolicy
    workflow_cron_schedule: str
    workflow_retry_policy: WorkflowRetryPolicy
    InitialSearchAttributes: dict[str, Any]
