from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_attribute_value_type import SearchAttributeValueType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchAttribute")


@_attrs_define
class SearchAttribute:
    """
    Attributes:
        key (Union[Unset, str]):
        string_value (Union[Unset, str]):
        integer_value (Union[Unset, int]):
        double_value (Union[Unset, float]):
        bool_value (Union[Unset, bool]):
        string_array_value (Union[Unset, list[str]]):
        value_type (Union[Unset, SearchAttributeValueType]):
    """

    key: Union[Unset, str] = UNSET
    string_value: Union[Unset, str] = UNSET
    integer_value: Union[Unset, int] = UNSET
    double_value: Union[Unset, float] = UNSET
    bool_value: Union[Unset, bool] = UNSET
    string_array_value: Union[Unset, list[str]] = UNSET
    value_type: Union[Unset, SearchAttributeValueType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        string_value = self.string_value

        integer_value = self.integer_value

        double_value = self.double_value

        bool_value = self.bool_value

        string_array_value: Union[Unset, list[str]] = UNSET
        if not isinstance(self.string_array_value, Unset):
            string_array_value = self.string_array_value

        value_type: Union[Unset, str] = UNSET
        if not isinstance(self.value_type, Unset):
            value_type = self.value_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if string_value is not UNSET:
            field_dict["stringValue"] = string_value
        if integer_value is not UNSET:
            field_dict["integerValue"] = integer_value
        if double_value is not UNSET:
            field_dict["doubleValue"] = double_value
        if bool_value is not UNSET:
            field_dict["boolValue"] = bool_value
        if string_array_value is not UNSET:
            field_dict["stringArrayValue"] = string_array_value
        if value_type is not UNSET:
            field_dict["valueType"] = value_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key", UNSET)

        string_value = d.pop("stringValue", UNSET)

        integer_value = d.pop("integerValue", UNSET)

        double_value = d.pop("doubleValue", UNSET)

        bool_value = d.pop("boolValue", UNSET)

        string_array_value = cast(list[str], d.pop("stringArrayValue", UNSET))

        _value_type = d.pop("valueType", UNSET)
        value_type: Union[Unset, SearchAttributeValueType]
        if isinstance(_value_type, Unset):
            value_type = UNSET
        else:
            value_type = SearchAttributeValueType(_value_type)

        search_attribute = cls(
            key=key,
            string_value=string_value,
            integer_value=integer_value,
            double_value=double_value,
            bool_value=bool_value,
            string_array_value=string_array_value,
            value_type=value_type,
        )

        search_attribute.additional_properties = d
        return search_attribute

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
