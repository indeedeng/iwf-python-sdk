from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject


T = TypeVar("T", bound="WorkflowSignalRequest")


@_attrs_define
class WorkflowSignalRequest:
    """
    Attributes:
        workflow_id (str):
        signal_channel_name (str):
        workflow_run_id (Union[Unset, str]):
        signal_value (Union[Unset, EncodedObject]):
    """

    workflow_id: str
    signal_channel_name: str
    workflow_run_id: Union[Unset, str] = UNSET
    signal_value: Union[Unset, "EncodedObject"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        signal_channel_name = self.signal_channel_name

        workflow_run_id = self.workflow_run_id

        signal_value: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.signal_value, Unset):
            signal_value = self.signal_value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "signalChannelName": signal_channel_name,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id
        if signal_value is not UNSET:
            field_dict["signalValue"] = signal_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject

        d = dict(src_dict)
        workflow_id = d.pop("workflowId")

        signal_channel_name = d.pop("signalChannelName")

        workflow_run_id = d.pop("workflowRunId", UNSET)

        _signal_value = d.pop("signalValue", UNSET)
        signal_value: Union[Unset, EncodedObject]
        if isinstance(_signal_value, Unset):
            signal_value = UNSET
        else:
            signal_value = EncodedObject.from_dict(_signal_value)

        workflow_signal_request = cls(
            workflow_id=workflow_id,
            signal_channel_name=signal_channel_name,
            workflow_run_id=workflow_run_id,
            signal_value=signal_value,
        )

        workflow_signal_request.additional_properties = d
        return workflow_signal_request

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
