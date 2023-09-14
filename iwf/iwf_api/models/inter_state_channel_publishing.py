from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject


T = TypeVar("T", bound="InterStateChannelPublishing")


@attr.s(auto_attribs=True)
class InterStateChannelPublishing:
    """
    Attributes:
        channel_name (str):
        value (Union[Unset, EncodedObject]):
    """

    channel_name: str
    value: Union[Unset, "EncodedObject"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel_name = self.channel_name
        value: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channelName": channel_name,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject

        d = src_dict.copy()
        channel_name = d.pop("channelName")

        _value = d.pop("value", UNSET)
        value: Union[Unset, EncodedObject]
        if isinstance(_value, Unset):
            value = UNSET
        else:
            value = EncodedObject.from_dict(_value)

        inter_state_channel_publishing = cls(
            channel_name=channel_name,
            value=value,
        )

        inter_state_channel_publishing.additional_properties = d
        return inter_state_channel_publishing

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
