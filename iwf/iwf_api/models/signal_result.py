from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.channel_request_status import ChannelRequestStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject


T = TypeVar("T", bound="SignalResult")


@_attrs_define
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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command_id = self.command_id

        signal_request_status = self.signal_request_status.value

        signal_channel_name = self.signal_channel_name

        signal_value: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.signal_value, Unset):
            signal_value = self.signal_value.to_dict()

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject

        d = dict(src_dict)
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
