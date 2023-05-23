from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowStartResponse")


@attr.s(auto_attribs=True)
class WorkflowStartResponse:
    """
    Attributes:
        workflow_run_id (Union[Unset, str]):
    """

    workflow_run_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_run_id = self.workflow_run_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_run_id = d.pop("workflowRunId", UNSET)

        workflow_start_response = cls(
            workflow_run_id=workflow_run_id,
        )

        workflow_start_response.additional_properties = d
        return workflow_start_response

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
