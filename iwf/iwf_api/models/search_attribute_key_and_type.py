from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_attribute_value_type import SearchAttributeValueType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchAttributeKeyAndType")


@_attrs_define
class SearchAttributeKeyAndType:
    """
    Attributes:
        key (Union[Unset, str]):
        value_type (Union[Unset, SearchAttributeValueType]):
    """

    key: Union[Unset, str] = UNSET
    value_type: Union[Unset, SearchAttributeValueType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value_type: Union[Unset, str] = UNSET
        if not isinstance(self.value_type, Unset):
            value_type = self.value_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if value_type is not UNSET:
            field_dict["valueType"] = value_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key", UNSET)

        _value_type = d.pop("valueType", UNSET)
        value_type: Union[Unset, SearchAttributeValueType]
        if isinstance(_value_type, Unset):
            value_type = UNSET
        else:
            value_type = SearchAttributeValueType(_value_type)

        search_attribute_key_and_type = cls(
            key=key,
            value_type=value_type,
        )

        search_attribute_key_and_type.additional_properties = d
        return search_attribute_key_and_type

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
