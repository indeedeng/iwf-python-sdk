from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.state_movement import StateMovement
    from ..models.workflow_conditional_close import WorkflowConditionalClose


T = TypeVar("T", bound="StateDecision")


@_attrs_define
class StateDecision:
    """
    Attributes:
        next_states (Union[Unset, list['StateMovement']]):
        conditional_close (Union[Unset, WorkflowConditionalClose]):
    """

    next_states: Union[Unset, list["StateMovement"]] = UNSET
    conditional_close: Union[Unset, "WorkflowConditionalClose"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        next_states: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.next_states, Unset):
            next_states = []
            for next_states_item_data in self.next_states:
                next_states_item = next_states_item_data.to_dict()
                next_states.append(next_states_item)

        conditional_close: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.conditional_close, Unset):
            conditional_close = self.conditional_close.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if next_states is not UNSET:
            field_dict["nextStates"] = next_states
        if conditional_close is not UNSET:
            field_dict["conditionalClose"] = conditional_close

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.state_movement import StateMovement
        from ..models.workflow_conditional_close import WorkflowConditionalClose

        d = dict(src_dict)
        next_states = []
        _next_states = d.pop("nextStates", UNSET)
        for next_states_item_data in _next_states or []:
            next_states_item = StateMovement.from_dict(next_states_item_data)

            next_states.append(next_states_item)

        _conditional_close = d.pop("conditionalClose", UNSET)
        conditional_close: Union[Unset, WorkflowConditionalClose]
        if isinstance(_conditional_close, Unset):
            conditional_close = UNSET
        else:
            conditional_close = WorkflowConditionalClose.from_dict(_conditional_close)

        state_decision = cls(
            next_states=next_states,
            conditional_close=conditional_close,
        )

        state_decision.additional_properties = d
        return state_decision

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
