from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TimerCommand")


@_attrs_define
class TimerCommand:
    """
    Attributes:
        duration_seconds (int):
        command_id (Union[Unset, str]):
    """

    duration_seconds: int
    command_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration_seconds = self.duration_seconds

        command_id = self.command_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "durationSeconds": duration_seconds,
            }
        )
        if command_id is not UNSET:
            field_dict["commandId"] = command_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        duration_seconds = d.pop("durationSeconds")

        command_id = d.pop("commandId", UNSET)

        timer_command = cls(
            duration_seconds=duration_seconds,
            command_id=command_id,
        )

        timer_command.additional_properties = d
        return timer_command

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
