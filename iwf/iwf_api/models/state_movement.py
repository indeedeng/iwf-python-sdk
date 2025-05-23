from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject
    from ..models.workflow_state_options import WorkflowStateOptions


T = TypeVar("T", bound="StateMovement")


@_attrs_define
class StateMovement:
    """
    Attributes:
        state_id (str):
        state_input (Union[Unset, EncodedObject]):
        state_options (Union[Unset, WorkflowStateOptions]):
        wait_for_key (Union[Unset, str]):
    """

    state_id: str
    state_input: Union[Unset, "EncodedObject"] = UNSET
    state_options: Union[Unset, "WorkflowStateOptions"] = UNSET
    wait_for_key: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state_id = self.state_id

        state_input: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.state_input, Unset):
            state_input = self.state_input.to_dict()

        state_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.state_options, Unset):
            state_options = self.state_options.to_dict()

        wait_for_key = self.wait_for_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stateId": state_id,
            }
        )
        if state_input is not UNSET:
            field_dict["stateInput"] = state_input
        if state_options is not UNSET:
            field_dict["stateOptions"] = state_options
        if wait_for_key is not UNSET:
            field_dict["waitForKey"] = wait_for_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject
        from ..models.workflow_state_options import WorkflowStateOptions

        d = dict(src_dict)
        state_id = d.pop("stateId")

        _state_input = d.pop("stateInput", UNSET)
        state_input: Union[Unset, EncodedObject]
        if isinstance(_state_input, Unset):
            state_input = UNSET
        else:
            state_input = EncodedObject.from_dict(_state_input)

        _state_options = d.pop("stateOptions", UNSET)
        state_options: Union[Unset, WorkflowStateOptions]
        if isinstance(_state_options, Unset):
            state_options = UNSET
        else:
            state_options = WorkflowStateOptions.from_dict(_state_options)

        wait_for_key = d.pop("waitForKey", UNSET)

        state_movement = cls(
            state_id=state_id,
            state_input=state_input,
            state_options=state_options,
            wait_for_key=wait_for_key,
        )

        state_movement.additional_properties = d
        return state_movement

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
