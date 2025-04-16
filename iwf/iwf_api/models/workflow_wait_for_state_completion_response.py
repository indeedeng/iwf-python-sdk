from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.state_completion_output import StateCompletionOutput


T = TypeVar("T", bound="WorkflowWaitForStateCompletionResponse")


@_attrs_define
class WorkflowWaitForStateCompletionResponse:
    """
    Attributes:
        state_completion_output (Union[Unset, StateCompletionOutput]):
    """

    state_completion_output: Union[Unset, "StateCompletionOutput"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state_completion_output: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.state_completion_output, Unset):
            state_completion_output = self.state_completion_output.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state_completion_output is not UNSET:
            field_dict["stateCompletionOutput"] = state_completion_output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.state_completion_output import StateCompletionOutput

        d = dict(src_dict)
        _state_completion_output = d.pop("stateCompletionOutput", UNSET)
        state_completion_output: Union[Unset, StateCompletionOutput]
        if isinstance(_state_completion_output, Unset):
            state_completion_output = UNSET
        else:
            state_completion_output = StateCompletionOutput.from_dict(_state_completion_output)

        workflow_wait_for_state_completion_response = cls(
            state_completion_output=state_completion_output,
        )

        workflow_wait_for_state_completion_response.additional_properties = d
        return workflow_wait_for_state_completion_response

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
