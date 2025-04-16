from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_search_response_entry import WorkflowSearchResponseEntry


T = TypeVar("T", bound="WorkflowSearchResponse")


@_attrs_define
class WorkflowSearchResponse:
    """
    Attributes:
        workflow_executions (Union[Unset, list['WorkflowSearchResponseEntry']]):
        next_page_token (Union[Unset, str]):
    """

    workflow_executions: Union[Unset, list["WorkflowSearchResponseEntry"]] = UNSET
    next_page_token: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_executions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.workflow_executions, Unset):
            workflow_executions = []
            for workflow_executions_item_data in self.workflow_executions:
                workflow_executions_item = workflow_executions_item_data.to_dict()
                workflow_executions.append(workflow_executions_item)

        next_page_token = self.next_page_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if workflow_executions is not UNSET:
            field_dict["workflowExecutions"] = workflow_executions
        if next_page_token is not UNSET:
            field_dict["nextPageToken"] = next_page_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workflow_search_response_entry import WorkflowSearchResponseEntry

        d = dict(src_dict)
        workflow_executions = []
        _workflow_executions = d.pop("workflowExecutions", UNSET)
        for workflow_executions_item_data in _workflow_executions or []:
            workflow_executions_item = WorkflowSearchResponseEntry.from_dict(workflow_executions_item_data)

            workflow_executions.append(workflow_executions_item)

        next_page_token = d.pop("nextPageToken", UNSET)

        workflow_search_response = cls(
            workflow_executions=workflow_executions,
            next_page_token=next_page_token,
        )

        workflow_search_response.additional_properties = d
        return workflow_search_response

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
