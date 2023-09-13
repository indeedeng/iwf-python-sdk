from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="SignalCommand")


@attr.s(auto_attribs=True)
class SignalCommand:
    """
    Attributes:
        command_id (str):
        signal_channel_name (str):
    """

    command_id: str
    signal_channel_name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command_id = self.command_id
        signal_channel_name = self.signal_channel_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "commandId": command_id,
                "signalChannelName": signal_channel_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        command_id = d.pop("commandId")

        signal_channel_name = d.pop("signalChannelName")

        signal_command = cls(
            command_id=command_id,
            signal_channel_name=signal_channel_name,
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
