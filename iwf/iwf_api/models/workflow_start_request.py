from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject
    from ..models.workflow_start_options import WorkflowStartOptions
    from ..models.workflow_state_options import WorkflowStateOptions


T = TypeVar("T", bound="WorkflowStartRequest")


@attr.s(auto_attribs=True)
class WorkflowStartRequest:
    """
    Attributes:
        workflow_id (str):
        iwf_workflow_type (str):
        workflow_timeout_seconds (int):
        iwf_worker_url (str):
        start_state_id (Union[Unset, str]):
        wait_for_completion_state_ids (Union[Unset, List[str]]):
        wait_for_completion_state_execution_ids (Union[Unset, List[str]]):
        state_input (Union[Unset, EncodedObject]):
        state_options (Union[Unset, WorkflowStateOptions]):
        workflow_start_options (Union[Unset, WorkflowStartOptions]):
    """

    workflow_id: str
    iwf_workflow_type: str
    workflow_timeout_seconds: int
    iwf_worker_url: str
    start_state_id: Union[Unset, str] = UNSET
    wait_for_completion_state_ids: Union[Unset, List[str]] = UNSET
    wait_for_completion_state_execution_ids: Union[Unset, List[str]] = UNSET
    state_input: Union[Unset, "EncodedObject"] = UNSET
    state_options: Union[Unset, "WorkflowStateOptions"] = UNSET
    workflow_start_options: Union[Unset, "WorkflowStartOptions"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id
        iwf_workflow_type = self.iwf_workflow_type
        workflow_timeout_seconds = self.workflow_timeout_seconds
        iwf_worker_url = self.iwf_worker_url
        start_state_id = self.start_state_id
        wait_for_completion_state_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.wait_for_completion_state_ids, Unset):
            wait_for_completion_state_ids = self.wait_for_completion_state_ids

        wait_for_completion_state_execution_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.wait_for_completion_state_execution_ids, Unset):
            wait_for_completion_state_execution_ids = (
                self.wait_for_completion_state_execution_ids
            )

        state_input: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.state_input, Unset):
            state_input = self.state_input.to_dict()

        state_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.state_options, Unset):
            state_options = self.state_options.to_dict()

        workflow_start_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_start_options, Unset):
            workflow_start_options = self.workflow_start_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "iwfWorkflowType": iwf_workflow_type,
                "workflowTimeoutSeconds": workflow_timeout_seconds,
                "iwfWorkerUrl": iwf_worker_url,
            }
        )
        if start_state_id is not UNSET:
            field_dict["startStateId"] = start_state_id
        if wait_for_completion_state_ids is not UNSET:
            field_dict["waitForCompletionStateIds"] = wait_for_completion_state_ids
        if wait_for_completion_state_execution_ids is not UNSET:
            field_dict["waitForCompletionStateExecutionIds"] = (
                wait_for_completion_state_execution_ids
            )
        if state_input is not UNSET:
            field_dict["stateInput"] = state_input
        if state_options is not UNSET:
            field_dict["stateOptions"] = state_options
        if workflow_start_options is not UNSET:
            field_dict["workflowStartOptions"] = workflow_start_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject
        from ..models.workflow_start_options import WorkflowStartOptions
        from ..models.workflow_state_options import WorkflowStateOptions

        d = src_dict.copy()
        workflow_id = d.pop("workflowId")

        iwf_workflow_type = d.pop("iwfWorkflowType")

        workflow_timeout_seconds = d.pop("workflowTimeoutSeconds")

        iwf_worker_url = d.pop("iwfWorkerUrl")

        start_state_id = d.pop("startStateId", UNSET)

        wait_for_completion_state_ids = cast(
            List[str], d.pop("waitForCompletionStateIds", UNSET)
        )

        wait_for_completion_state_execution_ids = cast(
            List[str], d.pop("waitForCompletionStateExecutionIds", UNSET)
        )

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

        _workflow_start_options = d.pop("workflowStartOptions", UNSET)
        workflow_start_options: Union[Unset, WorkflowStartOptions]
        if isinstance(_workflow_start_options, Unset):
            workflow_start_options = UNSET
        else:
            workflow_start_options = WorkflowStartOptions.from_dict(
                _workflow_start_options
            )

        workflow_start_request = cls(
            workflow_id=workflow_id,
            iwf_workflow_type=iwf_workflow_type,
            workflow_timeout_seconds=workflow_timeout_seconds,
            iwf_worker_url=iwf_worker_url,
            start_state_id=start_state_id,
            wait_for_completion_state_ids=wait_for_completion_state_ids,
            wait_for_completion_state_execution_ids=wait_for_completion_state_execution_ids,
            state_input=state_input,
            state_options=state_options,
            workflow_start_options=workflow_start_options,
        )

        workflow_start_request.additional_properties = d
        return workflow_start_request

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
