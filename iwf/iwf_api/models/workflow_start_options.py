from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.id_reuse_policy import IDReusePolicy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.key_value import KeyValue
    from ..models.search_attribute import SearchAttribute
    from ..models.workflow_already_started_options import WorkflowAlreadyStartedOptions
    from ..models.workflow_config import WorkflowConfig
    from ..models.workflow_retry_policy import WorkflowRetryPolicy


T = TypeVar("T", bound="WorkflowStartOptions")


@attr.s(auto_attribs=True)
class WorkflowStartOptions:
    """
    Attributes:
        id_reuse_policy (Union[Unset, IDReusePolicy]):
        cron_schedule (Union[Unset, str]):
        workflow_start_delay_seconds (Union[Unset, int]):
        retry_policy (Union[Unset, WorkflowRetryPolicy]):
        search_attributes (Union[Unset, List['SearchAttribute']]):
        data_attributes (Union[Unset, List['KeyValue']]):
        workflow_config_override (Union[Unset, WorkflowConfig]):
        use_memo_for_data_attributes (Union[Unset, bool]):
        workflow_already_started_options (Union[Unset, WorkflowAlreadyStartedOptions]):
    """

    id_reuse_policy: Union[Unset, IDReusePolicy] = UNSET
    cron_schedule: Union[Unset, str] = UNSET
    workflow_start_delay_seconds: Union[Unset, int] = UNSET
    retry_policy: Union[Unset, "WorkflowRetryPolicy"] = UNSET
    search_attributes: Union[Unset, List["SearchAttribute"]] = UNSET
    data_attributes: Union[Unset, List["KeyValue"]] = UNSET
    workflow_config_override: Union[Unset, "WorkflowConfig"] = UNSET
    use_memo_for_data_attributes: Union[Unset, bool] = UNSET
    workflow_already_started_options: Union[Unset, "WorkflowAlreadyStartedOptions"] = (
        UNSET
    )
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_reuse_policy: Union[Unset, str] = UNSET
        if not isinstance(self.id_reuse_policy, Unset):
            id_reuse_policy = self.id_reuse_policy.value

        cron_schedule = self.cron_schedule
        workflow_start_delay_seconds = self.workflow_start_delay_seconds
        retry_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry_policy, Unset):
            retry_policy = self.retry_policy.to_dict()

        search_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.search_attributes, Unset):
            search_attributes = []
            for search_attributes_item_data in self.search_attributes:
                search_attributes_item = search_attributes_item_data.to_dict()

                search_attributes.append(search_attributes_item)

        data_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data_attributes, Unset):
            data_attributes = []
            for data_attributes_item_data in self.data_attributes:
                data_attributes_item = data_attributes_item_data.to_dict()

                data_attributes.append(data_attributes_item)

        workflow_config_override: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_config_override, Unset):
            workflow_config_override = self.workflow_config_override.to_dict()

        use_memo_for_data_attributes = self.use_memo_for_data_attributes
        workflow_already_started_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_already_started_options, Unset):
            workflow_already_started_options = (
                self.workflow_already_started_options.to_dict()
            )

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id_reuse_policy is not UNSET:
            field_dict["idReusePolicy"] = id_reuse_policy
        if cron_schedule is not UNSET:
            field_dict["cronSchedule"] = cron_schedule
        if workflow_start_delay_seconds is not UNSET:
            field_dict["workflowStartDelaySeconds"] = workflow_start_delay_seconds
        if retry_policy is not UNSET:
            field_dict["retryPolicy"] = retry_policy
        if search_attributes is not UNSET:
            field_dict["searchAttributes"] = search_attributes
        if data_attributes is not UNSET:
            field_dict["dataAttributes"] = data_attributes
        if workflow_config_override is not UNSET:
            field_dict["workflowConfigOverride"] = workflow_config_override
        if use_memo_for_data_attributes is not UNSET:
            field_dict["useMemoForDataAttributes"] = use_memo_for_data_attributes
        if workflow_already_started_options is not UNSET:
            field_dict["workflowAlreadyStartedOptions"] = (
                workflow_already_started_options
            )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.key_value import KeyValue
        from ..models.search_attribute import SearchAttribute
        from ..models.workflow_already_started_options import (
            WorkflowAlreadyStartedOptions,
        )
        from ..models.workflow_config import WorkflowConfig
        from ..models.workflow_retry_policy import WorkflowRetryPolicy

        d = src_dict.copy()
        _id_reuse_policy = d.pop("idReusePolicy", UNSET)
        id_reuse_policy: Union[Unset, IDReusePolicy]
        if isinstance(_id_reuse_policy, Unset):
            id_reuse_policy = UNSET
        else:
            id_reuse_policy = IDReusePolicy(_id_reuse_policy)

        cron_schedule = d.pop("cronSchedule", UNSET)

        workflow_start_delay_seconds = d.pop("workflowStartDelaySeconds", UNSET)

        _retry_policy = d.pop("retryPolicy", UNSET)
        retry_policy: Union[Unset, WorkflowRetryPolicy]
        if isinstance(_retry_policy, Unset):
            retry_policy = UNSET
        else:
            retry_policy = WorkflowRetryPolicy.from_dict(_retry_policy)

        search_attributes = []
        _search_attributes = d.pop("searchAttributes", UNSET)
        for search_attributes_item_data in _search_attributes or []:
            search_attributes_item = SearchAttribute.from_dict(
                search_attributes_item_data
            )

            search_attributes.append(search_attributes_item)

        data_attributes = []
        _data_attributes = d.pop("dataAttributes", UNSET)
        for data_attributes_item_data in _data_attributes or []:
            data_attributes_item = KeyValue.from_dict(data_attributes_item_data)

            data_attributes.append(data_attributes_item)

        _workflow_config_override = d.pop("workflowConfigOverride", UNSET)
        workflow_config_override: Union[Unset, WorkflowConfig]
        if isinstance(_workflow_config_override, Unset):
            workflow_config_override = UNSET
        else:
            workflow_config_override = WorkflowConfig.from_dict(
                _workflow_config_override
            )

        use_memo_for_data_attributes = d.pop("useMemoForDataAttributes", UNSET)

        _workflow_already_started_options = d.pop(
            "workflowAlreadyStartedOptions", UNSET
        )
        workflow_already_started_options: Union[Unset, WorkflowAlreadyStartedOptions]
        if isinstance(_workflow_already_started_options, Unset):
            workflow_already_started_options = UNSET
        else:
            workflow_already_started_options = WorkflowAlreadyStartedOptions.from_dict(
                _workflow_already_started_options
            )

        workflow_start_options = cls(
            id_reuse_policy=id_reuse_policy,
            cron_schedule=cron_schedule,
            workflow_start_delay_seconds=workflow_start_delay_seconds,
            retry_policy=retry_policy,
            search_attributes=search_attributes,
            data_attributes=data_attributes,
            workflow_config_override=workflow_config_override,
            use_memo_for_data_attributes=use_memo_for_data_attributes,
            workflow_already_started_options=workflow_already_started_options,
        )

        workflow_start_options.additional_properties = d
        return workflow_start_options

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
