from dataclasses import dataclass
from typing import Any, Optional

from iwf_api.models import (
    ExecuteApiFailurePolicy,
    PersistenceLoadingPolicy,
    RetryPolicy,
    WaitUntilApiFailurePolicy,
    WorkflowStateOptions as IdlWorkflowStateOptions,
)


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
    """
        note that the failing handling state will take the same input as the failed state
        the type is Optional[type[WorkflowState]] but there is an issue with type hint...
        TODO fix this type hint
    """
    execute_failure_handling_state: Optional[type] = None


def _to_idl_state_options(
    skip_wait_until: bool,
    options: Any,  # TODO this type was Optional[WorkflowStateOptions],
    # however, type hint is not working with recursive call...
    state_store: dict[str, Any],  # TODO this type should be dict[str, WorkflowState]
) -> IdlWorkflowStateOptions:
    res = IdlWorkflowStateOptions()
    if skip_wait_until:
        res.skip_wait_until = True

    if options is None:
        return res
    assert isinstance(options, WorkflowStateOptions)

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
    if options.execute_failure_handling_state is not None:
        res.execute_api_failure_policy = (
            ExecuteApiFailurePolicy.PROCEED_TO_CONFIGURED_STATE
        )
        from iwf.workflow_state import get_state_id_by_class

        res.execute_api_failure_proceed_state_id = get_state_id_by_class(
            options.execute_failure_handling_state
        )
        state = state_store[res.execute_api_failure_proceed_state_id]
        proceed_state_options = state.get_state_options()

        from iwf.workflow_state import should_skip_wait_until

        proceed_state_idl_options = _to_idl_state_options(
            should_skip_wait_until(state), proceed_state_options, state_store
        )
        res.execute_api_failure_proceed_state_options = proceed_state_idl_options
    return res
