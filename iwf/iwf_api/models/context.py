from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Context")


@_attrs_define
class Context:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (str):
        workflow_started_timestamp (int):
        state_execution_id (Union[Unset, str]):
        first_attempt_timestamp (Union[Unset, int]):
        attempt (Union[Unset, int]):
    """

    workflow_id: str
    workflow_run_id: str
    workflow_started_timestamp: int
    state_execution_id: Union[Unset, str] = UNSET
    first_attempt_timestamp: Union[Unset, int] = UNSET
    attempt: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        workflow_run_id = self.workflow_run_id

        workflow_started_timestamp = self.workflow_started_timestamp

        state_execution_id = self.state_execution_id

        first_attempt_timestamp = self.first_attempt_timestamp

        attempt = self.attempt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "workflowRunId": workflow_run_id,
                "workflowStartedTimestamp": workflow_started_timestamp,
            }
        )
        if state_execution_id is not UNSET:
            field_dict["stateExecutionId"] = state_execution_id
        if first_attempt_timestamp is not UNSET:
            field_dict["firstAttemptTimestamp"] = first_attempt_timestamp
        if attempt is not UNSET:
            field_dict["attempt"] = attempt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId")

        workflow_started_timestamp = d.pop("workflowStartedTimestamp")

        state_execution_id = d.pop("stateExecutionId", UNSET)

        first_attempt_timestamp = d.pop("firstAttemptTimestamp", UNSET)

        attempt = d.pop("attempt", UNSET)

        context = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            workflow_started_timestamp=workflow_started_timestamp,
            state_execution_id=state_execution_id,
            first_attempt_timestamp=first_attempt_timestamp,
            attempt=attempt,
        )

        context.additional_properties = d
        return context

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
