from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HealthInfo")


@_attrs_define
class HealthInfo:
    """
    Attributes:
        condition (Union[Unset, str]):
        hostname (Union[Unset, str]):
        duration (Union[Unset, int]):
    """

    condition: Union[Unset, str] = UNSET
    hostname: Union[Unset, str] = UNSET
    duration: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        condition = self.condition

        hostname = self.hostname

        duration = self.duration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if condition is not UNSET:
            field_dict["condition"] = condition
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if duration is not UNSET:
            field_dict["duration"] = duration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        condition = d.pop("condition", UNSET)

        hostname = d.pop("hostname", UNSET)

        duration = d.pop("duration", UNSET)

        health_info = cls(
            condition=condition,
            hostname=hostname,
            duration=duration,
        )

        health_info.additional_properties = d
        return health_info

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
