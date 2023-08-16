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
    state_id: Optional[str] = None
    search_attributes_loading_policy: Optional[PersistenceLoadingPolicy] = None
    data_attributes_loading_policy: Optional[PersistenceLoadingPolicy] = None
    wait_until_api_timeout_seconds: Optional[int] = None
    execute_api_timeout_seconds: Optional[int] = None
    wait_until_api_retry_policy: Optional[RetryPolicy] = None
    execute_api_retry_policy: Optional[RetryPolicy] = None
    wait_until_api_failure_policy: Optional[WaitUntilApiFailurePolicy] = None


def to_idl_state_options(
    options: Optional[WorkflowStateOptions],
) -> IdlWorkflowStateOptions:
    res = IdlWorkflowStateOptions()
    if options is None:
        return res
    if options.search_attributes_loading_policy is not None:
        res.search_attributes_loading_policy = options.search_attributes_loading_policy
    if options.data_attributes_loading_policy is not None:
        res.data_attributes_loading_policy = options.data_attributes_loading_policy
    if options.wait_until_api_failure_policy is not None:
        res.wait_until_api_failure_policy = options.wait_until_api_failure_policy
    if options.wait_until_api_retry_policy is not None:
        res.wait_until_api_retry_policy = options.wait_until_api_retry_policy
    if options.wait_until_api_timeout_seconds is not None:
        res.wait_until_api_timeout_seconds = options.wait_until_api_timeout_seconds
    if options.execute_api_retry_policy is not None:
        res.execute_api_retry_policy = options.execute_api_retry_policy
    if options.execute_api_timeout_seconds is not None:
        res.execute_api_timeout_seconds = options.execute_api_timeout_seconds
    return res
