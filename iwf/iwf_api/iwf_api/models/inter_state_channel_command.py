from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="InterStateChannelCommand")


@attr.s(auto_attribs=True)
class InterStateChannelCommand:
    """
    Attributes:
        command_id (str):
        channel_name (str):
    """

    command_id: str
    channel_name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command_id = self.command_id
        channel_name = self.channel_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "commandId": command_id,
                "channelName": channel_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        command_id = d.pop("commandId")

        channel_name = d.pop("channelName")

        inter_state_channel_command = cls(
            command_id=command_id,
            channel_name=channel_name,
        )

        inter_state_channel_command.additional_properties = d
        return inter_state_channel_command

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
