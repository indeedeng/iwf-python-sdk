from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkflowSearchResponseEntry")


@_attrs_define
class WorkflowSearchResponseEntry:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (str):
    """

    workflow_id: str
    workflow_run_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        workflow_run_id = self.workflow_run_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "workflowRunId": workflow_run_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId")

        workflow_search_response_entry = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
        )

        workflow_search_response_entry.additional_properties = d
        return workflow_search_response_entry

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
