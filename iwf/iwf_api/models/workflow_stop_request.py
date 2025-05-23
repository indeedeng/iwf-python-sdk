from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workflow_stop_type import WorkflowStopType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowStopRequest")


@_attrs_define
class WorkflowStopRequest:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (Union[Unset, str]):
        reason (Union[Unset, str]):
        stop_type (Union[Unset, WorkflowStopType]):
    """

    workflow_id: str
    workflow_run_id: Union[Unset, str] = UNSET
    reason: Union[Unset, str] = UNSET
    stop_type: Union[Unset, WorkflowStopType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        workflow_run_id = self.workflow_run_id

        reason = self.reason

        stop_type: Union[Unset, str] = UNSET
        if not isinstance(self.stop_type, Unset):
            stop_type = self.stop_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id
        if reason is not UNSET:
            field_dict["reason"] = reason
        if stop_type is not UNSET:
            field_dict["stopType"] = stop_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId", UNSET)

        reason = d.pop("reason", UNSET)

        _stop_type = d.pop("stopType", UNSET)
        stop_type: Union[Unset, WorkflowStopType]
        if isinstance(_stop_type, Unset):
            stop_type = UNSET
        else:
            stop_type = WorkflowStopType(_stop_type)

        workflow_stop_request = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            reason=reason,
            stop_type=stop_type,
        )

        workflow_stop_request.additional_properties = d
        return workflow_stop_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
