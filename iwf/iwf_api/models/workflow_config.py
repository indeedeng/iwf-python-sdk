from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.workflow_config_executing_state_id_mode import (
    WorkflowConfigExecutingStateIdMode,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowConfig")


@attr.s(auto_attribs=True)
class WorkflowConfig:
    """
    Attributes:
        disable_system_search_attribute (Union[Unset, bool]):
        executing_state_id_mode (Union[Unset, WorkflowConfigExecutingStateIdMode]):
        continue_as_new_threshold (Union[Unset, int]):
        continue_as_new_page_size_in_bytes (Union[Unset, int]):
        optimize_activity (Union[Unset, bool]):
    """

    disable_system_search_attribute: Union[Unset, bool] = UNSET
    executing_state_id_mode: Union[Unset, WorkflowConfigExecutingStateIdMode] = UNSET
    continue_as_new_threshold: Union[Unset, int] = UNSET
    continue_as_new_page_size_in_bytes: Union[Unset, int] = UNSET
    optimize_activity: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        disable_system_search_attribute = self.disable_system_search_attribute
        executing_state_id_mode: Union[Unset, str] = UNSET
        if not isinstance(self.executing_state_id_mode, Unset):
            executing_state_id_mode = self.executing_state_id_mode.value

        continue_as_new_threshold = self.continue_as_new_threshold
        continue_as_new_page_size_in_bytes = self.continue_as_new_page_size_in_bytes
        optimize_activity = self.optimize_activity

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if disable_system_search_attribute is not UNSET:
            field_dict["disableSystemSearchAttribute"] = disable_system_search_attribute
        if executing_state_id_mode is not UNSET:
            field_dict["executingStateIdMode"] = executing_state_id_mode
        if continue_as_new_threshold is not UNSET:
            field_dict["continueAsNewThreshold"] = continue_as_new_threshold
        if continue_as_new_page_size_in_bytes is not UNSET:
            field_dict["continueAsNewPageSizeInBytes"] = (
                continue_as_new_page_size_in_bytes
            )
        if optimize_activity is not UNSET:
            field_dict["optimizeActivity"] = optimize_activity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        disable_system_search_attribute = d.pop("disableSystemSearchAttribute", UNSET)

        _executing_state_id_mode = d.pop("executingStateIdMode", UNSET)
        executing_state_id_mode: Union[Unset, WorkflowConfigExecutingStateIdMode]
        if isinstance(_executing_state_id_mode, Unset):
            executing_state_id_mode = UNSET
        else:
            executing_state_id_mode = WorkflowConfigExecutingStateIdMode(
                _executing_state_id_mode
            )

        continue_as_new_threshold = d.pop("continueAsNewThreshold", UNSET)

        continue_as_new_page_size_in_bytes = d.pop(
            "continueAsNewPageSizeInBytes", UNSET
        )

        optimize_activity = d.pop("optimizeActivity", UNSET)

        workflow_config = cls(
            disable_system_search_attribute=disable_system_search_attribute,
            executing_state_id_mode=executing_state_id_mode,
            continue_as_new_threshold=continue_as_new_threshold,
            continue_as_new_page_size_in_bytes=continue_as_new_page_size_in_bytes,
            optimize_activity=optimize_activity,
        )

        workflow_config.additional_properties = d
        return workflow_config

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
