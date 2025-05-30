from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.executing_state_id_mode import ExecutingStateIdMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowConfig")


@_attrs_define
class WorkflowConfig:
    """
    Attributes:
        executing_state_id_mode (Union[Unset, ExecutingStateIdMode]):
        continue_as_new_threshold (Union[Unset, int]):
        continue_as_new_page_size_in_bytes (Union[Unset, int]):
        optimize_activity (Union[Unset, bool]):
        optimize_timer (Union[Unset, bool]):
    """

    executing_state_id_mode: Union[Unset, ExecutingStateIdMode] = UNSET
    continue_as_new_threshold: Union[Unset, int] = UNSET
    continue_as_new_page_size_in_bytes: Union[Unset, int] = UNSET
    optimize_activity: Union[Unset, bool] = UNSET
    optimize_timer: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        executing_state_id_mode: Union[Unset, str] = UNSET
        if not isinstance(self.executing_state_id_mode, Unset):
            executing_state_id_mode = self.executing_state_id_mode.value

        continue_as_new_threshold = self.continue_as_new_threshold

        continue_as_new_page_size_in_bytes = self.continue_as_new_page_size_in_bytes

        optimize_activity = self.optimize_activity

        optimize_timer = self.optimize_timer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if executing_state_id_mode is not UNSET:
            field_dict["executingStateIdMode"] = executing_state_id_mode
        if continue_as_new_threshold is not UNSET:
            field_dict["continueAsNewThreshold"] = continue_as_new_threshold
        if continue_as_new_page_size_in_bytes is not UNSET:
            field_dict["continueAsNewPageSizeInBytes"] = continue_as_new_page_size_in_bytes
        if optimize_activity is not UNSET:
            field_dict["optimizeActivity"] = optimize_activity
        if optimize_timer is not UNSET:
            field_dict["optimizeTimer"] = optimize_timer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _executing_state_id_mode = d.pop("executingStateIdMode", UNSET)
        executing_state_id_mode: Union[Unset, ExecutingStateIdMode]
        if isinstance(_executing_state_id_mode, Unset):
            executing_state_id_mode = UNSET
        else:
            executing_state_id_mode = ExecutingStateIdMode(_executing_state_id_mode)

        continue_as_new_threshold = d.pop("continueAsNewThreshold", UNSET)

        continue_as_new_page_size_in_bytes = d.pop("continueAsNewPageSizeInBytes", UNSET)

        optimize_activity = d.pop("optimizeActivity", UNSET)

        optimize_timer = d.pop("optimizeTimer", UNSET)

        workflow_config = cls(
            executing_state_id_mode=executing_state_id_mode,
            continue_as_new_threshold=continue_as_new_threshold,
            continue_as_new_page_size_in_bytes=continue_as_new_page_size_in_bytes,
            optimize_activity=optimize_activity,
            optimize_timer=optimize_timer,
        )

        workflow_config.additional_properties = d
        return workflow_config

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
