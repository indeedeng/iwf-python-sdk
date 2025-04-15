from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowWaitForStateCompletionRequest")


@_attrs_define
class WorkflowWaitForStateCompletionRequest:
    """
    Attributes:
        workflow_id (str):
        state_execution_id (Union[Unset, str]):
        state_id (Union[Unset, str]):
        wait_for_key (Union[Unset, str]):
        wait_time_seconds (Union[Unset, int]):
    """

    workflow_id: str
    state_execution_id: Union[Unset, str] = UNSET
    state_id: Union[Unset, str] = UNSET
    wait_for_key: Union[Unset, str] = UNSET
    wait_time_seconds: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        state_execution_id = self.state_execution_id

        state_id = self.state_id

        wait_for_key = self.wait_for_key

        wait_time_seconds = self.wait_time_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
            }
        )
        if state_execution_id is not UNSET:
            field_dict["stateExecutionId"] = state_execution_id
        if state_id is not UNSET:
            field_dict["stateId"] = state_id
        if wait_for_key is not UNSET:
            field_dict["waitForKey"] = wait_for_key
        if wait_time_seconds is not UNSET:
            field_dict["waitTimeSeconds"] = wait_time_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workflow_id = d.pop("workflowId")

        state_execution_id = d.pop("stateExecutionId", UNSET)

        state_id = d.pop("stateId", UNSET)

        wait_for_key = d.pop("waitForKey", UNSET)

        wait_time_seconds = d.pop("waitTimeSeconds", UNSET)

        workflow_wait_for_state_completion_request = cls(
            workflow_id=workflow_id,
            state_execution_id=state_execution_id,
            state_id=state_id,
            wait_for_key=wait_for_key,
            wait_time_seconds=wait_time_seconds,
        )

        workflow_wait_for_state_completion_request.additional_properties = d
        return workflow_wait_for_state_completion_request

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
