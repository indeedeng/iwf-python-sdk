from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workflow_conditional_close_type import WorkflowConditionalCloseType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject


T = TypeVar("T", bound="WorkflowConditionalClose")


@_attrs_define
class WorkflowConditionalClose:
    """
    Attributes:
        conditional_close_type (Union[Unset, WorkflowConditionalCloseType]):
        channel_name (Union[Unset, str]):
        close_input (Union[Unset, EncodedObject]):
    """

    conditional_close_type: Union[Unset, WorkflowConditionalCloseType] = UNSET
    channel_name: Union[Unset, str] = UNSET
    close_input: Union[Unset, "EncodedObject"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        conditional_close_type: Union[Unset, str] = UNSET
        if not isinstance(self.conditional_close_type, Unset):
            conditional_close_type = self.conditional_close_type.value

        channel_name = self.channel_name

        close_input: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.close_input, Unset):
            close_input = self.close_input.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conditional_close_type is not UNSET:
            field_dict["conditionalCloseType"] = conditional_close_type
        if channel_name is not UNSET:
            field_dict["channelName"] = channel_name
        if close_input is not UNSET:
            field_dict["closeInput"] = close_input

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject

        d = dict(src_dict)
        _conditional_close_type = d.pop("conditionalCloseType", UNSET)
        conditional_close_type: Union[Unset, WorkflowConditionalCloseType]
        if isinstance(_conditional_close_type, Unset):
            conditional_close_type = UNSET
        else:
            conditional_close_type = WorkflowConditionalCloseType(_conditional_close_type)

        channel_name = d.pop("channelName", UNSET)

        _close_input = d.pop("closeInput", UNSET)
        close_input: Union[Unset, EncodedObject]
        if isinstance(_close_input, Unset):
            close_input = UNSET
        else:
            close_input = EncodedObject.from_dict(_close_input)

        workflow_conditional_close = cls(
            conditional_close_type=conditional_close_type,
            channel_name=channel_name,
            close_input=close_input,
        )

        workflow_conditional_close.additional_properties = d
        return workflow_conditional_close

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
