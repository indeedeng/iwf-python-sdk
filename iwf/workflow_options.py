from dataclasses import dataclass
from typing import Any, Optional

from iwf.iwf_api.models import (
    IDReusePolicy,
    WorkflowRetryPolicy,
    WorkflowAlreadyStartedOptions,
    WorkflowConfig,
)


@dataclass
class WorkflowOptions:
    workflow_id_reuse_policy: Optional[IDReusePolicy] = None
    workflow_cron_schedule: Optional[str] = None
    workflow_start_delay_seconds: Optional[int] = None
    workflow_retry_policy: Optional[WorkflowRetryPolicy] = None
    workflow_already_started_options: Optional[WorkflowAlreadyStartedOptions] = None
    workflow_config_override: Optional[WorkflowConfig] = None
    initial_data_attributes: Optional[dict[str, Any]] = None
