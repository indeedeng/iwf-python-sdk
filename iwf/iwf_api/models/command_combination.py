from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CommandCombination")


@_attrs_define
class CommandCombination:
    """
    Attributes:
        command_ids (Union[Unset, list[str]]):
    """

    command_ids: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.command_ids, Unset):
            command_ids = self.command_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command_ids is not UNSET:
            field_dict["commandIds"] = command_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        command_ids = cast(list[str], d.pop("commandIds", UNSET))

        command_combination = cls(
            command_ids=command_ids,
        )

        command_combination.additional_properties = d
        return command_combination

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
