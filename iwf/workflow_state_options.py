from dataclasses import dataclass
from typing import Optional

from iwf_api.models import (
    PersistenceLoadingPolicy,
    RetryPolicy,
    WaitUntilApiFailurePolicy,
)
from iwf_api.models import WorkflowStateOptions as IdlWorkflowStateOptions


@dataclass
class WorkflowStateOptions:
    state_id: Optional[str]
    search_attributes_loading_policy: Optional[PersistenceLoadingPolicy]
    data_attributes_loading_policy: Optional[PersistenceLoadingPolicy]
    wait_until_api_timeout_seconds: Optional[int]
    execute_api_timeout_seconds: Optional[int]
    wait_until_api_retry_policy: Optional[RetryPolicy]
    execute_api_retry_policy: Optional[RetryPolicy]
    wait_until_api_failure_policy: Optional[WaitUntilApiFailurePolicy]


def to_idl_state_options(options: WorkflowStateOptions) -> IdlWorkflowStateOptions:
    return IdlWorkflowStateOptions(
        search_attributes_loading_policy=options.search_attributes_loading_policy,
        data_attributes_loading_policy=options.data_attributes_loading_policy,
        wait_until_api_failure_policy=options.wait_until_api_failure_policy,
        wait_until_api_retry_policy=options.wait_until_api_retry_policy,
        wait_until_api_timeout_seconds=options.wait_until_api_timeout_seconds,
        execute_api_retry_policy=options.execute_api_retry_policy,
        execute_api_timeout_seconds=options.execute_api_timeout_seconds,
    )
