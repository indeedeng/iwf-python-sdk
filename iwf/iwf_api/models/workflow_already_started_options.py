from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowAlreadyStartedOptions")


@_attrs_define
class WorkflowAlreadyStartedOptions:
    """
    Attributes:
        ignore_already_started_error (bool):
        request_id (Union[Unset, str]):
    """

    ignore_already_started_error: bool
    request_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ignore_already_started_error = self.ignore_already_started_error

        request_id = self.request_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ignoreAlreadyStartedError": ignore_already_started_error,
            }
        )
        if request_id is not UNSET:
            field_dict["requestId"] = request_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ignore_already_started_error = d.pop("ignoreAlreadyStartedError")

        request_id = d.pop("requestId", UNSET)

        workflow_already_started_options = cls(
            ignore_already_started_error=ignore_already_started_error,
            request_id=request_id,
        )

        workflow_already_started_options.additional_properties = d
        return workflow_already_started_options

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
