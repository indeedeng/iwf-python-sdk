from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowGetDataObjectsRequest")


@attr.s(auto_attribs=True)
class WorkflowGetDataObjectsRequest:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (Union[Unset, str]):
        keys (Union[Unset, List[str]]):
        use_memo_for_data_attributes (Union[Unset, bool]):
    """

    workflow_id: str
    workflow_run_id: Union[Unset, str] = UNSET
    keys: Union[Unset, List[str]] = UNSET
    use_memo_for_data_attributes: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id
        workflow_run_id = self.workflow_run_id
        keys: Union[Unset, List[str]] = UNSET
        if not isinstance(self.keys, Unset):
            keys = self.keys

        use_memo_for_data_attributes = self.use_memo_for_data_attributes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id
        if keys is not UNSET:
            field_dict["keys"] = keys
        if use_memo_for_data_attributes is not UNSET:
            field_dict["useMemoForDataAttributes"] = use_memo_for_data_attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId", UNSET)

        keys = cast(List[str], d.pop("keys", UNSET))

        use_memo_for_data_attributes = d.pop("useMemoForDataAttributes", UNSET)

        workflow_get_data_objects_request = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            keys=keys,
            use_memo_for_data_attributes=use_memo_for_data_attributes,
        )

        workflow_get_data_objects_request.additional_properties = d
        return workflow_get_data_objects_request

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
