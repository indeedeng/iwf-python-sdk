from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkflowResetResponse")


@attr.s(auto_attribs=True)
class WorkflowResetResponse:
    """
    Attributes:
        workflow_run_id (str):
    """

    workflow_run_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_run_id = self.workflow_run_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowRunId": workflow_run_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_run_id = d.pop("workflowRunId")

        workflow_reset_response = cls(
            workflow_run_id=workflow_run_id,
        )

        workflow_reset_response.additional_properties = d
        return workflow_reset_response

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
