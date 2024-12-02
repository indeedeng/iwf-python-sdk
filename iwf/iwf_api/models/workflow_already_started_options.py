from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowAlreadyStartedOptions")


@attr.s(auto_attribs=True)
class WorkflowAlreadyStartedOptions:
    """
    Attributes:
        ignore_already_started_error (bool):
        request_id (Union[Unset, str]):
    """

    ignore_already_started_error: bool
    request_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ignore_already_started_error = self.ignore_already_started_error
        request_id = self.request_id

        field_dict: Dict[str, Any] = {}
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ignore_already_started_error = d.pop("ignoreAlreadyStartedError")

        request_id = d.pop("requestId", UNSET)

        workflow_already_started_options = cls(
            ignore_already_started_error=ignore_already_started_error,
            request_id=request_id,
        )

        workflow_already_started_options.additional_properties = d
        return workflow_already_started_options

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
