from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject


T = TypeVar("T", bound="StateCompletionOutput")


@_attrs_define
class StateCompletionOutput:
    """
    Attributes:
        completed_state_id (str):
        completed_state_execution_id (str):
        completed_state_output (Union[Unset, EncodedObject]):
    """

    completed_state_id: str
    completed_state_execution_id: str
    completed_state_output: Union[Unset, "EncodedObject"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        completed_state_id = self.completed_state_id

        completed_state_execution_id = self.completed_state_execution_id

        completed_state_output: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.completed_state_output, Unset):
            completed_state_output = self.completed_state_output.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completedStateId": completed_state_id,
                "completedStateExecutionId": completed_state_execution_id,
            }
        )
        if completed_state_output is not UNSET:
            field_dict["completedStateOutput"] = completed_state_output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject

        d = dict(src_dict)
        completed_state_id = d.pop("completedStateId")

        completed_state_execution_id = d.pop("completedStateExecutionId")

        _completed_state_output = d.pop("completedStateOutput", UNSET)
        completed_state_output: Union[Unset, EncodedObject]
        if isinstance(_completed_state_output, Unset):
            completed_state_output = UNSET
        else:
            completed_state_output = EncodedObject.from_dict(_completed_state_output)

        state_completion_output = cls(
            completed_state_id=completed_state_id,
            completed_state_execution_id=completed_state_execution_id,
            completed_state_output=completed_state_output,
        )

        state_completion_output.additional_properties = d
        return state_completion_output

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
