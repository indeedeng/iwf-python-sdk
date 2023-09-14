from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_config import WorkflowConfig


T = TypeVar("T", bound="WorkflowConfigUpdateRequest")


@attr.s(auto_attribs=True)
class WorkflowConfigUpdateRequest:
    """
    Attributes:
        workflow_id (str):
        workflow_config (WorkflowConfig):
        workflow_run_id (Union[Unset, str]):
    """

    workflow_id: str
    workflow_config: "WorkflowConfig"
    workflow_run_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id
        workflow_config = self.workflow_config.to_dict()

        workflow_run_id = self.workflow_run_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "workflowConfig": workflow_config,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workflow_config import WorkflowConfig

        d = src_dict.copy()
        workflow_id = d.pop("workflowId")

        workflow_config = WorkflowConfig.from_dict(d.pop("workflowConfig"))

        workflow_run_id = d.pop("workflowRunId", UNSET)

        workflow_config_update_request = cls(
            workflow_id=workflow_id,
            workflow_config=workflow_config,
            workflow_run_id=workflow_run_id,
        )

        workflow_config_update_request.additional_properties = d
        return workflow_config_update_request

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
