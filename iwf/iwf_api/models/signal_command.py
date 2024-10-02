from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SignalCommand")


@attr.s(auto_attribs=True)
class SignalCommand:
    """
    Attributes:
        signal_channel_name (str):
        command_id (Union[Unset, str]):
        at_least (Union[Unset, int]):
        at_most (Union[Unset, int]):
    """

    signal_channel_name: str
    command_id: Union[Unset, str] = UNSET
    at_least: Union[Unset, int] = UNSET
    at_most: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        signal_channel_name = self.signal_channel_name
        command_id = self.command_id
        at_least = self.at_least
        at_most = self.at_most

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "signalChannelName": signal_channel_name,
            }
        )
        if command_id is not UNSET:
            field_dict["commandId"] = command_id
        if at_least is not UNSET:
            field_dict["atLeast"] = at_least
        if at_most is not UNSET:
            field_dict["atMost"] = at_most

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        signal_channel_name = d.pop("signalChannelName")

        command_id = d.pop("commandId", UNSET)

        at_least = d.pop("atLeast", UNSET)

        at_most = d.pop("atMost", UNSET)

        signal_command = cls(
            signal_channel_name=signal_channel_name,
            command_id=command_id,
            at_least=at_least,
            at_most=at_most,
        )

        signal_command.additional_properties = d
        return signal_command

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
