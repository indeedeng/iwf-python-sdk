from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkflowDumpRequest")


@attr.s(auto_attribs=True)
class WorkflowDumpRequest:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (str):
        page_size_in_bytes (int):
        page_num (int):
    """

    workflow_id: str
    workflow_run_id: str
    page_size_in_bytes: int
    page_num: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id
        workflow_run_id = self.workflow_run_id
        page_size_in_bytes = self.page_size_in_bytes
        page_num = self.page_num

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "workflowRunId": workflow_run_id,
                "pageSizeInBytes": page_size_in_bytes,
                "pageNum": page_num,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId")

        page_size_in_bytes = d.pop("pageSizeInBytes")

        page_num = d.pop("pageNum")

        workflow_dump_request = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            page_size_in_bytes=page_size_in_bytes,
            page_num=page_num,
        )

        workflow_dump_request.additional_properties = d
        return workflow_dump_request

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
