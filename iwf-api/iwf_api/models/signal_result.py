from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.channel_request_status import ChannelRequestStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject


T = TypeVar("T", bound="SignalResult")


@attr.s(auto_attribs=True)
class SignalResult:
    """
    Attributes:
        command_id (str):
        signal_request_status (ChannelRequestStatus):
        signal_channel_name (str):
        signal_value (Union[Unset, EncodedObject]):
    """

    command_id: str
    signal_request_status: ChannelRequestStatus
    signal_channel_name: str
    signal_value: Union[Unset, "EncodedObject"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command_id = self.command_id
        signal_request_status = self.signal_request_status.value

        signal_channel_name = self.signal_channel_name
        signal_value: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.signal_value, Unset):
            signal_value = self.signal_value.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "commandId": command_id,
                "signalRequestStatus": signal_request_status,
                "signalChannelName": signal_channel_name,
            }
        )
        if signal_value is not UNSET:
            field_dict["signalValue"] = signal_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject

        d = src_dict.copy()
        command_id = d.pop("commandId")

        signal_request_status = ChannelRequestStatus(d.pop("signalRequestStatus"))

        signal_channel_name = d.pop("signalChannelName")

        _signal_value = d.pop("signalValue", UNSET)
        signal_value: Union[Unset, EncodedObject]
        if isinstance(_signal_value, Unset):
            signal_value = UNSET
        else:
            signal_value = EncodedObject.from_dict(_signal_value)

        signal_result = cls(
            command_id=command_id,
            signal_request_status=signal_request_status,
            signal_channel_name=signal_channel_name,
            signal_value=signal_value,
        )

        signal_result.additional_properties = d
        return signal_result

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
