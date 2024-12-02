from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.workflow_reset_type import WorkflowResetType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowResetRequest")


@attr.s(auto_attribs=True)
class WorkflowResetRequest:
    """
    Attributes:
        workflow_id (str):
        reset_type (WorkflowResetType):
        workflow_run_id (Union[Unset, str]):
        history_event_id (Union[Unset, int]):
        reason (Union[Unset, str]):
        history_event_time (Union[Unset, str]):
        state_id (Union[Unset, str]):
        state_execution_id (Union[Unset, str]):
        skip_signal_reapply (Union[Unset, bool]):
        skip_update_reapply (Union[Unset, bool]):
    """

    workflow_id: str
    reset_type: WorkflowResetType
    workflow_run_id: Union[Unset, str] = UNSET
    history_event_id: Union[Unset, int] = UNSET
    reason: Union[Unset, str] = UNSET
    history_event_time: Union[Unset, str] = UNSET
    state_id: Union[Unset, str] = UNSET
    state_execution_id: Union[Unset, str] = UNSET
    skip_signal_reapply: Union[Unset, bool] = UNSET
    skip_update_reapply: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id
        reset_type = self.reset_type.value

        workflow_run_id = self.workflow_run_id
        history_event_id = self.history_event_id
        reason = self.reason
        history_event_time = self.history_event_time
        state_id = self.state_id
        state_execution_id = self.state_execution_id
        skip_signal_reapply = self.skip_signal_reapply
        skip_update_reapply = self.skip_update_reapply

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "resetType": reset_type,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id
        if history_event_id is not UNSET:
            field_dict["historyEventId"] = history_event_id
        if reason is not UNSET:
            field_dict["reason"] = reason
        if history_event_time is not UNSET:
            field_dict["historyEventTime"] = history_event_time
        if state_id is not UNSET:
            field_dict["stateId"] = state_id
        if state_execution_id is not UNSET:
            field_dict["stateExecutionId"] = state_execution_id
        if skip_signal_reapply is not UNSET:
            field_dict["skipSignalReapply"] = skip_signal_reapply
        if skip_update_reapply is not UNSET:
            field_dict["skipUpdateReapply"] = skip_update_reapply

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_id = d.pop("workflowId")

        reset_type = WorkflowResetType(d.pop("resetType"))

        workflow_run_id = d.pop("workflowRunId", UNSET)

        history_event_id = d.pop("historyEventId", UNSET)

        reason = d.pop("reason", UNSET)

        history_event_time = d.pop("historyEventTime", UNSET)

        state_id = d.pop("stateId", UNSET)

        state_execution_id = d.pop("stateExecutionId", UNSET)

        skip_signal_reapply = d.pop("skipSignalReapply", UNSET)

        skip_update_reapply = d.pop("skipUpdateReapply", UNSET)

        workflow_reset_request = cls(
            workflow_id=workflow_id,
            reset_type=reset_type,
            workflow_run_id=workflow_run_id,
            history_event_id=history_event_id,
            reason=reason,
            history_event_time=history_event_time,
            state_id=state_id,
            state_execution_id=state_execution_id,
            skip_signal_reapply=skip_signal_reapply,
            skip_update_reapply=skip_update_reapply,
        )

        workflow_reset_request.additional_properties = d
        return workflow_reset_request

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
