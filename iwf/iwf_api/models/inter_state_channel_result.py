from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.channel_request_status import ChannelRequestStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject


T = TypeVar("T", bound="InterStateChannelResult")


@_attrs_define
class InterStateChannelResult:
    """
    Attributes:
        command_id (str):
        request_status (ChannelRequestStatus):
        channel_name (str):
        value (Union[Unset, EncodedObject]):
    """

    command_id: str
    request_status: ChannelRequestStatus
    channel_name: str
    value: Union[Unset, "EncodedObject"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command_id = self.command_id

        request_status = self.request_status.value

        channel_name = self.channel_name

        value: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "commandId": command_id,
                "requestStatus": request_status,
                "channelName": channel_name,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject

        d = dict(src_dict)
        command_id = d.pop("commandId")

        request_status = ChannelRequestStatus(d.pop("requestStatus"))

        channel_name = d.pop("channelName")

        _value = d.pop("value", UNSET)
        value: Union[Unset, EncodedObject]
        if isinstance(_value, Unset):
            value = UNSET
        else:
            value = EncodedObject.from_dict(_value)

        inter_state_channel_result = cls(
            command_id=command_id,
            request_status=request_status,
            channel_name=channel_name,
            value=value,
        )

        inter_state_channel_result.additional_properties = d
        return inter_state_channel_result

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
