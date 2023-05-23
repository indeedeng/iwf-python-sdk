from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EncodedObject")


@attr.s(auto_attribs=True)
class EncodedObject:
    """
    Attributes:
        encoding (Union[Unset, str]):
        data (Union[Unset, str]):
    """

    encoding: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        encoding = self.encoding
        data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if encoding is not UNSET:
            field_dict["encoding"] = encoding
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        encoding = d.pop("encoding", UNSET)

        data = d.pop("data", UNSET)

        encoded_object = cls(
            encoding=encoding,
            data=data,
        )

        encoded_object.additional_properties = d
        return encoded_object

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
