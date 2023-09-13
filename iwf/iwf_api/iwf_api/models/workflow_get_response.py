from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.workflow_error_type import WorkflowErrorType
from ..models.workflow_status import WorkflowStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.state_completion_output import StateCompletionOutput


T = TypeVar("T", bound="WorkflowGetResponse")


@attr.s(auto_attribs=True)
class WorkflowGetResponse:
    """
    Attributes:
        workflow_run_id (str):
        workflow_status (WorkflowStatus):
        results (Union[Unset, List['StateCompletionOutput']]):
        error_type (Union[Unset, WorkflowErrorType]):
        error_message (Union[Unset, str]):
    """

    workflow_run_id: str
    workflow_status: WorkflowStatus
    results: Union[Unset, List["StateCompletionOutput"]] = UNSET
    error_type: Union[Unset, WorkflowErrorType] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_run_id = self.workflow_run_id
        workflow_status = self.workflow_status.value

        results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()

                results.append(results_item)

        error_type: Union[Unset, str] = UNSET
        if not isinstance(self.error_type, Unset):
            error_type = self.error_type.value

        error_message = self.error_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowRunId": workflow_run_id,
                "workflowStatus": workflow_status,
            }
        )
        if results is not UNSET:
            field_dict["results"] = results
        if error_type is not UNSET:
            field_dict["errorType"] = error_type
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.state_completion_output import StateCompletionOutput

        d = src_dict.copy()
        workflow_run_id = d.pop("workflowRunId")

        workflow_status = WorkflowStatus(d.pop("workflowStatus"))

        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = StateCompletionOutput.from_dict(results_item_data)

            results.append(results_item)

        _error_type = d.pop("errorType", UNSET)
        error_type: Union[Unset, WorkflowErrorType]
        if isinstance(_error_type, Unset):
            error_type = UNSET
        else:
            error_type = WorkflowErrorType(_error_type)

        error_message = d.pop("errorMessage", UNSET)

        workflow_get_response = cls(
            workflow_run_id=workflow_run_id,
            workflow_status=workflow_status,
            results=results,
            error_type=error_type,
            error_message=error_message,
        )

        workflow_get_response.additional_properties = d
        return workflow_get_response

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
