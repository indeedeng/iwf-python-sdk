from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_attribute_key_and_type import SearchAttributeKeyAndType


T = TypeVar("T", bound="WorkflowGetSearchAttributesRequest")


@attr.s(auto_attribs=True)
class WorkflowGetSearchAttributesRequest:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (Union[Unset, str]):
        keys (Union[Unset, List['SearchAttributeKeyAndType']]):
    """

    workflow_id: str
    workflow_run_id: Union[Unset, str] = UNSET
    keys: Union[Unset, List["SearchAttributeKeyAndType"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id
        workflow_run_id = self.workflow_run_id
        keys: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.keys, Unset):
            keys = []
            for keys_item_data in self.keys:
                keys_item = keys_item_data.to_dict()

                keys.append(keys_item)

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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.search_attribute_key_and_type import SearchAttributeKeyAndType

        d = src_dict.copy()
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId", UNSET)

        keys = []
        _keys = d.pop("keys", UNSET)
        for keys_item_data in _keys or []:
            keys_item = SearchAttributeKeyAndType.from_dict(keys_item_data)

            keys.append(keys_item)

        workflow_get_search_attributes_request = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            keys=keys,
        )

        workflow_get_search_attributes_request.additional_properties = d
        return workflow_get_search_attributes_request

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
