from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkflowSearchResponseEntry")


@attr.s(auto_attribs=True)
class WorkflowSearchResponseEntry:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (str):
    """

    workflow_id: str
    workflow_run_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id
        workflow_run_id = self.workflow_run_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "workflowRunId": workflow_run_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId")

        workflow_search_response_entry = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
        )

        workflow_search_response_entry.additional_properties = d
        return workflow_search_response_entry

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
