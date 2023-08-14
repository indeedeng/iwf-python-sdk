from dataclasses import dataclass

from iwf_api.models import (
    PersistenceLoadingPolicy,
    RetryPolicy,
    WaitUntilApiFailurePolicy,
)


@dataclass
class WorkflowStateOptions:
    search_attributes_loading_policy: PersistenceLoadingPolicy
    data_attributes_loading_policy: PersistenceLoadingPolicy
    wait_until_api_timeout_seconds: int
    execute_api_timeout_seconds: int
    wait_until_api_retry_policy: RetryPolicy
    execute_api_retry_policy: RetryPolicy
    wait_until_api_failure_policy: WaitUntilApiFailurePolicy
