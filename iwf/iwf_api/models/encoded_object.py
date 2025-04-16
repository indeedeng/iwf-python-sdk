from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EncodedObject")


@_attrs_define
class EncodedObject:
    """
    Attributes:
        encoding (Union[Unset, str]):
        data (Union[Unset, str]):
    """

    encoding: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        encoding = self.encoding

        data = self.data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if encoding is not UNSET:
            field_dict["encoding"] = encoding
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        encoding = d.pop("encoding", UNSET)

        data = d.pop("data", UNSET)

        encoded_object = cls(
            encoding=encoding,
            data=data,
        )

        encoded_object.additional_properties = d
        return encoded_object

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
