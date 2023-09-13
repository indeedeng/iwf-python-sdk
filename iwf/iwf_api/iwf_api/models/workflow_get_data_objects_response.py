from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.key_value import KeyValue


T = TypeVar("T", bound="WorkflowGetDataObjectsResponse")


@attr.s(auto_attribs=True)
class WorkflowGetDataObjectsResponse:
    """
    Attributes:
        objects (Union[Unset, List['KeyValue']]):
    """

    objects: Union[Unset, List["KeyValue"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        objects: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.objects, Unset):
            objects = []
            for objects_item_data in self.objects:
                objects_item = objects_item_data.to_dict()

                objects.append(objects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if objects is not UNSET:
            field_dict["objects"] = objects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.key_value import KeyValue

        d = src_dict.copy()
        objects = []
        _objects = d.pop("objects", UNSET)
        for objects_item_data in _objects or []:
            objects_item = KeyValue.from_dict(objects_item_data)

            objects.append(objects_item)

        workflow_get_data_objects_response = cls(
            objects=objects,
        )

        workflow_get_data_objects_response.additional_properties = d
        return workflow_get_data_objects_response

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
