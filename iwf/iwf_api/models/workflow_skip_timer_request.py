from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowSkipTimerRequest")


@_attrs_define
class WorkflowSkipTimerRequest:
    """
    Attributes:
        workflow_id (str):
        workflow_state_execution_id (str):
        workflow_run_id (Union[Unset, str]):
        timer_command_id (Union[Unset, str]):
        timer_command_index (Union[Unset, int]):
    """

    workflow_id: str
    workflow_state_execution_id: str
    workflow_run_id: Union[Unset, str] = UNSET
    timer_command_id: Union[Unset, str] = UNSET
    timer_command_index: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        workflow_state_execution_id = self.workflow_state_execution_id

        workflow_run_id = self.workflow_run_id

        timer_command_id = self.timer_command_id

        timer_command_index = self.timer_command_index

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "workflowStateExecutionId": workflow_state_execution_id,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id
        if timer_command_id is not UNSET:
            field_dict["timerCommandId"] = timer_command_id
        if timer_command_index is not UNSET:
            field_dict["timerCommandIndex"] = timer_command_index

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workflow_id = d.pop("workflowId")

        workflow_state_execution_id = d.pop("workflowStateExecutionId")

        workflow_run_id = d.pop("workflowRunId", UNSET)

        timer_command_id = d.pop("timerCommandId", UNSET)

        timer_command_index = d.pop("timerCommandIndex", UNSET)

        workflow_skip_timer_request = cls(
            workflow_id=workflow_id,
            workflow_state_execution_id=workflow_state_execution_id,
            workflow_run_id=workflow_run_id,
            timer_command_id=timer_command_id,
            timer_command_index=timer_command_index,
        )

        workflow_skip_timer_request.additional_properties = d
        return workflow_skip_timer_request

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
