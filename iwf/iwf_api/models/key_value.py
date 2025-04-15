from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject


T = TypeVar("T", bound="KeyValue")


@_attrs_define
class KeyValue:
    """
    Attributes:
        key (Union[Unset, str]):
        value (Union[Unset, EncodedObject]):
    """

    key: Union[Unset, str] = UNSET
    value: Union[Unset, "EncodedObject"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject

        d = dict(src_dict)
        key = d.pop("key", UNSET)

        _value = d.pop("value", UNSET)
        value: Union[Unset, EncodedObject]
        if isinstance(_value, Unset):
            value = UNSET
        else:
            value = EncodedObject.from_dict(_value)

        key_value = cls(
            key=key,
            value=value,
        )

        key_value.additional_properties = d
        return key_value

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
