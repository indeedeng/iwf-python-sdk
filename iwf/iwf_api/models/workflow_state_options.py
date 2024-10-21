from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.execute_api_failure_policy import ExecuteApiFailurePolicy
from ..models.wait_until_api_failure_policy import WaitUntilApiFailurePolicy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.persistence_loading_policy import PersistenceLoadingPolicy
    from ..models.retry_policy import RetryPolicy


T = TypeVar("T", bound="WorkflowStateOptions")


@attr.s(auto_attribs=True)
class WorkflowStateOptions:
    """
    Attributes:
        search_attributes_loading_policy (Union[Unset, PersistenceLoadingPolicy]):
        wait_until_api_search_attributes_loading_policy (Union[Unset, PersistenceLoadingPolicy]):
        execute_api_search_attributes_loading_policy (Union[Unset, PersistenceLoadingPolicy]):
        data_attributes_loading_policy (Union[Unset, PersistenceLoadingPolicy]):
        wait_until_api_data_attributes_loading_policy (Union[Unset, PersistenceLoadingPolicy]):
        execute_api_data_attributes_loading_policy (Union[Unset, PersistenceLoadingPolicy]):
        wait_until_api_timeout_seconds (Union[Unset, int]):
        execute_api_timeout_seconds (Union[Unset, int]):
        wait_until_api_retry_policy (Union[Unset, RetryPolicy]):
        execute_api_retry_policy (Union[Unset, RetryPolicy]):
        wait_until_api_failure_policy (Union[Unset, WaitUntilApiFailurePolicy]):
        execute_api_failure_policy (Union[Unset, ExecuteApiFailurePolicy]):
        execute_api_failure_proceed_state_id (Union[Unset, str]):
        execute_api_failure_proceed_state_options (Union[Unset, WorkflowStateOptions]):
        skip_wait_until (Union[Unset, bool]):
    """

    search_attributes_loading_policy: Union[Unset, "PersistenceLoadingPolicy"] = UNSET
    wait_until_api_search_attributes_loading_policy: Union[
        Unset, "PersistenceLoadingPolicy"
    ] = UNSET
    execute_api_search_attributes_loading_policy: Union[
        Unset, "PersistenceLoadingPolicy"
    ] = UNSET
    data_attributes_loading_policy: Union[Unset, "PersistenceLoadingPolicy"] = UNSET
    wait_until_api_data_attributes_loading_policy: Union[
        Unset, "PersistenceLoadingPolicy"
    ] = UNSET
    execute_api_data_attributes_loading_policy: Union[
        Unset, "PersistenceLoadingPolicy"
    ] = UNSET
    wait_until_api_timeout_seconds: Union[Unset, int] = UNSET
    execute_api_timeout_seconds: Union[Unset, int] = UNSET
    wait_until_api_retry_policy: Union[Unset, "RetryPolicy"] = UNSET
    execute_api_retry_policy: Union[Unset, "RetryPolicy"] = UNSET
    wait_until_api_failure_policy: Union[Unset, WaitUntilApiFailurePolicy] = UNSET
    execute_api_failure_policy: Union[Unset, ExecuteApiFailurePolicy] = UNSET
    execute_api_failure_proceed_state_id: Union[Unset, str] = UNSET
    execute_api_failure_proceed_state_options: Union[Unset, "WorkflowStateOptions"] = (
        UNSET
    )
    skip_wait_until: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        search_attributes_loading_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.search_attributes_loading_policy, Unset):
            search_attributes_loading_policy = (
                self.search_attributes_loading_policy.to_dict()
            )

        wait_until_api_search_attributes_loading_policy: Union[
            Unset, Dict[str, Any]
        ] = UNSET
        if not isinstance(self.wait_until_api_search_attributes_loading_policy, Unset):
            wait_until_api_search_attributes_loading_policy = (
                self.wait_until_api_search_attributes_loading_policy.to_dict()
            )

        execute_api_search_attributes_loading_policy: Union[Unset, Dict[str, Any]] = (
            UNSET
        )
        if not isinstance(self.execute_api_search_attributes_loading_policy, Unset):
            execute_api_search_attributes_loading_policy = (
                self.execute_api_search_attributes_loading_policy.to_dict()
            )

        data_attributes_loading_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data_attributes_loading_policy, Unset):
            data_attributes_loading_policy = (
                self.data_attributes_loading_policy.to_dict()
            )

        wait_until_api_data_attributes_loading_policy: Union[Unset, Dict[str, Any]] = (
            UNSET
        )
        if not isinstance(self.wait_until_api_data_attributes_loading_policy, Unset):
            wait_until_api_data_attributes_loading_policy = (
                self.wait_until_api_data_attributes_loading_policy.to_dict()
            )

        execute_api_data_attributes_loading_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.execute_api_data_attributes_loading_policy, Unset):
            execute_api_data_attributes_loading_policy = (
                self.execute_api_data_attributes_loading_policy.to_dict()
            )

        wait_until_api_timeout_seconds = self.wait_until_api_timeout_seconds
        execute_api_timeout_seconds = self.execute_api_timeout_seconds
        wait_until_api_retry_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.wait_until_api_retry_policy, Unset):
            wait_until_api_retry_policy = self.wait_until_api_retry_policy.to_dict()

        execute_api_retry_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.execute_api_retry_policy, Unset):
            execute_api_retry_policy = self.execute_api_retry_policy.to_dict()

        wait_until_api_failure_policy: Union[Unset, str] = UNSET
        if not isinstance(self.wait_until_api_failure_policy, Unset):
            wait_until_api_failure_policy = self.wait_until_api_failure_policy.value

        execute_api_failure_policy: Union[Unset, str] = UNSET
        if not isinstance(self.execute_api_failure_policy, Unset):
            execute_api_failure_policy = self.execute_api_failure_policy.value

        execute_api_failure_proceed_state_id = self.execute_api_failure_proceed_state_id
        execute_api_failure_proceed_state_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.execute_api_failure_proceed_state_options, Unset):
            execute_api_failure_proceed_state_options = (
                self.execute_api_failure_proceed_state_options.to_dict()
            )

        skip_wait_until = self.skip_wait_until

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if search_attributes_loading_policy is not UNSET:
            field_dict["searchAttributesLoadingPolicy"] = (
                search_attributes_loading_policy
            )
        if wait_until_api_search_attributes_loading_policy is not UNSET:
            field_dict["waitUntilApiSearchAttributesLoadingPolicy"] = (
                wait_until_api_search_attributes_loading_policy
            )
        if execute_api_search_attributes_loading_policy is not UNSET:
            field_dict["executeApiSearchAttributesLoadingPolicy"] = (
                execute_api_search_attributes_loading_policy
            )
        if data_attributes_loading_policy is not UNSET:
            field_dict["dataAttributesLoadingPolicy"] = data_attributes_loading_policy
        if wait_until_api_data_attributes_loading_policy is not UNSET:
            field_dict["waitUntilApiDataAttributesLoadingPolicy"] = (
                wait_until_api_data_attributes_loading_policy
            )
        if execute_api_data_attributes_loading_policy is not UNSET:
            field_dict["executeApiDataAttributesLoadingPolicy"] = (
                execute_api_data_attributes_loading_policy
            )
        if wait_until_api_timeout_seconds is not UNSET:
            field_dict["waitUntilApiTimeoutSeconds"] = wait_until_api_timeout_seconds
        if execute_api_timeout_seconds is not UNSET:
            field_dict["executeApiTimeoutSeconds"] = execute_api_timeout_seconds
        if wait_until_api_retry_policy is not UNSET:
            field_dict["waitUntilApiRetryPolicy"] = wait_until_api_retry_policy
        if execute_api_retry_policy is not UNSET:
            field_dict["executeApiRetryPolicy"] = execute_api_retry_policy
        if wait_until_api_failure_policy is not UNSET:
            field_dict["waitUntilApiFailurePolicy"] = wait_until_api_failure_policy
        if execute_api_failure_policy is not UNSET:
            field_dict["executeApiFailurePolicy"] = execute_api_failure_policy
        if execute_api_failure_proceed_state_id is not UNSET:
            field_dict["executeApiFailureProceedStateId"] = (
                execute_api_failure_proceed_state_id
            )
        if execute_api_failure_proceed_state_options is not UNSET:
            field_dict["executeApiFailureProceedStateOptions"] = (
                execute_api_failure_proceed_state_options
            )
        if skip_wait_until is not UNSET:
            field_dict["skipWaitUntil"] = skip_wait_until

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.persistence_loading_policy import PersistenceLoadingPolicy
        from ..models.retry_policy import RetryPolicy

        d = src_dict.copy()
        _search_attributes_loading_policy = d.pop(
            "searchAttributesLoadingPolicy", UNSET
        )
        search_attributes_loading_policy: Union[Unset, PersistenceLoadingPolicy]
        if isinstance(_search_attributes_loading_policy, Unset):
            search_attributes_loading_policy = UNSET
        else:
            search_attributes_loading_policy = PersistenceLoadingPolicy.from_dict(
                _search_attributes_loading_policy
            )

        _wait_until_api_search_attributes_loading_policy = d.pop(
            "waitUntilApiSearchAttributesLoadingPolicy", UNSET
        )
        wait_until_api_search_attributes_loading_policy: Union[
            Unset, PersistenceLoadingPolicy
        ]
        if isinstance(_wait_until_api_search_attributes_loading_policy, Unset):
            wait_until_api_search_attributes_loading_policy = UNSET
        else:
            wait_until_api_search_attributes_loading_policy = (
                PersistenceLoadingPolicy.from_dict(
                    _wait_until_api_search_attributes_loading_policy
                )
            )

        _execute_api_search_attributes_loading_policy = d.pop(
            "executeApiSearchAttributesLoadingPolicy", UNSET
        )
        execute_api_search_attributes_loading_policy: Union[
            Unset, PersistenceLoadingPolicy
        ]
        if isinstance(_execute_api_search_attributes_loading_policy, Unset):
            execute_api_search_attributes_loading_policy = UNSET
        else:
            execute_api_search_attributes_loading_policy = (
                PersistenceLoadingPolicy.from_dict(
                    _execute_api_search_attributes_loading_policy
                )
            )

        _data_attributes_loading_policy = d.pop("dataAttributesLoadingPolicy", UNSET)
        data_attributes_loading_policy: Union[Unset, PersistenceLoadingPolicy]
        if isinstance(_data_attributes_loading_policy, Unset):
            data_attributes_loading_policy = UNSET
        else:
            data_attributes_loading_policy = PersistenceLoadingPolicy.from_dict(
                _data_attributes_loading_policy
            )

        _wait_until_api_data_attributes_loading_policy = d.pop(
            "waitUntilApiDataAttributesLoadingPolicy", UNSET
        )
        wait_until_api_data_attributes_loading_policy: Union[
            Unset, PersistenceLoadingPolicy
        ]
        if isinstance(_wait_until_api_data_attributes_loading_policy, Unset):
            wait_until_api_data_attributes_loading_policy = UNSET
        else:
            wait_until_api_data_attributes_loading_policy = (
                PersistenceLoadingPolicy.from_dict(
                    _wait_until_api_data_attributes_loading_policy
                )
            )

        _execute_api_data_attributes_loading_policy = d.pop(
            "executeApiDataAttributesLoadingPolicy", UNSET
        )
        execute_api_data_attributes_loading_policy: Union[
            Unset, PersistenceLoadingPolicy
        ]
        if isinstance(_execute_api_data_attributes_loading_policy, Unset):
            execute_api_data_attributes_loading_policy = UNSET
        else:
            execute_api_data_attributes_loading_policy = (
                PersistenceLoadingPolicy.from_dict(
                    _execute_api_data_attributes_loading_policy
                )
            )

        wait_until_api_timeout_seconds = d.pop("waitUntilApiTimeoutSeconds", UNSET)

        execute_api_timeout_seconds = d.pop("executeApiTimeoutSeconds", UNSET)

        _wait_until_api_retry_policy = d.pop("waitUntilApiRetryPolicy", UNSET)
        wait_until_api_retry_policy: Union[Unset, RetryPolicy]
        if isinstance(_wait_until_api_retry_policy, Unset):
            wait_until_api_retry_policy = UNSET
        else:
            wait_until_api_retry_policy = RetryPolicy.from_dict(
                _wait_until_api_retry_policy
            )

        _execute_api_retry_policy = d.pop("executeApiRetryPolicy", UNSET)
        execute_api_retry_policy: Union[Unset, RetryPolicy]
        if isinstance(_execute_api_retry_policy, Unset):
            execute_api_retry_policy = UNSET
        else:
            execute_api_retry_policy = RetryPolicy.from_dict(_execute_api_retry_policy)

        _wait_until_api_failure_policy = d.pop("waitUntilApiFailurePolicy", UNSET)
        wait_until_api_failure_policy: Union[Unset, WaitUntilApiFailurePolicy]
        if isinstance(_wait_until_api_failure_policy, Unset):
            wait_until_api_failure_policy = UNSET
        else:
            wait_until_api_failure_policy = WaitUntilApiFailurePolicy(
                _wait_until_api_failure_policy
            )

        _execute_api_failure_policy = d.pop("executeApiFailurePolicy", UNSET)
        execute_api_failure_policy: Union[Unset, ExecuteApiFailurePolicy]
        if isinstance(_execute_api_failure_policy, Unset):
            execute_api_failure_policy = UNSET
        else:
            execute_api_failure_policy = ExecuteApiFailurePolicy(
                _execute_api_failure_policy
            )

        execute_api_failure_proceed_state_id = d.pop(
            "executeApiFailureProceedStateId", UNSET
        )

        _execute_api_failure_proceed_state_options = d.pop(
            "executeApiFailureProceedStateOptions", UNSET
        )
        execute_api_failure_proceed_state_options: Union[Unset, WorkflowStateOptions]
        if isinstance(_execute_api_failure_proceed_state_options, Unset):
            execute_api_failure_proceed_state_options = UNSET
        else:
            execute_api_failure_proceed_state_options = WorkflowStateOptions.from_dict(
                _execute_api_failure_proceed_state_options
            )

        skip_wait_until = d.pop("skipWaitUntil", UNSET)

        workflow_state_options = cls(
            search_attributes_loading_policy=search_attributes_loading_policy,
            wait_until_api_search_attributes_loading_policy=wait_until_api_search_attributes_loading_policy,
            execute_api_search_attributes_loading_policy=execute_api_search_attributes_loading_policy,
            data_attributes_loading_policy=data_attributes_loading_policy,
            wait_until_api_data_attributes_loading_policy=wait_until_api_data_attributes_loading_policy,
            execute_api_data_attributes_loading_policy=execute_api_data_attributes_loading_policy,
            wait_until_api_timeout_seconds=wait_until_api_timeout_seconds,
            execute_api_timeout_seconds=execute_api_timeout_seconds,
            wait_until_api_retry_policy=wait_until_api_retry_policy,
            execute_api_retry_policy=execute_api_retry_policy,
            wait_until_api_failure_policy=wait_until_api_failure_policy,
            execute_api_failure_policy=execute_api_failure_policy,
            execute_api_failure_proceed_state_id=execute_api_failure_proceed_state_id,
            execute_api_failure_proceed_state_options=execute_api_failure_proceed_state_options,
            skip_wait_until=skip_wait_until,
        )

        workflow_state_options.additional_properties = d
        return workflow_state_options

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
