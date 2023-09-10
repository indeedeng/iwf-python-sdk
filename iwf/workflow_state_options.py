from dataclasses import dataclass
from typing import Any, Optional

from iwf_api.models import (
    ExecuteApiFailurePolicy,
    PersistenceLoadingPolicy,
    RetryPolicy,
    WaitUntilApiFailurePolicy,
    WorkflowStateOptions as IdlWorkflowStateOptions,
)

from iwf.workflow_state import WorkflowState, get_state_id_by_class


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
    _execute_failure_handling_state: Optional[type[WorkflowState]] = None

    def set_execute_failure_recovery(self, failure_handling_state: type[WorkflowState]):
        """
        note that the failing handling state will take the same input as the failed state
        Args:
            failure_handling_state:

        Returns:

        """
        self._execute_failure_handling_state = failure_handling_state


def _to_idl_state_options(
    options: Any,  # TODO this type was Optional[WorkflowStateOptions],
    # however, type hint is not working with recursive call...
    state_store: dict[str, WorkflowState],
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
    if options._execute_failure_handling_state is not None:
        res.execute_api_failure_policy = (
            ExecuteApiFailurePolicy.FAIL_WORKFLOW_ON_EXECUTE_API_FAILURE
        )
        res.execute_api_failure_proceed_state_id = get_state_id_by_class(
            options._execute_failure_handling_state
        )
        state = state_store[res.execute_api_failure_proceed_state_id]
        proceed_state_options = state.get_state_options()
        proceed_state_idl_options = _to_idl_state_options(
            proceed_state_options, state_store
        )
        res.execute_api_failure_proceed_state_options = proceed_state_idl_options
    return res
