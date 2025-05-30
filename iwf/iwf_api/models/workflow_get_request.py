from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowGetRequest")


@_attrs_define
class WorkflowGetRequest:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (Union[Unset, str]):
        needs_results (Union[Unset, bool]):
        wait_time_seconds (Union[Unset, int]):
    """

    workflow_id: str
    workflow_run_id: Union[Unset, str] = UNSET
    needs_results: Union[Unset, bool] = UNSET
    wait_time_seconds: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        workflow_run_id = self.workflow_run_id

        needs_results = self.needs_results

        wait_time_seconds = self.wait_time_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id
        if needs_results is not UNSET:
            field_dict["needsResults"] = needs_results
        if wait_time_seconds is not UNSET:
            field_dict["waitTimeSeconds"] = wait_time_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId", UNSET)

        needs_results = d.pop("needsResults", UNSET)

        wait_time_seconds = d.pop("waitTimeSeconds", UNSET)

        workflow_get_request = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            needs_results=needs_results,
            wait_time_seconds=wait_time_seconds,
        )

        workflow_get_request.additional_properties = d
        return workflow_get_request

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
