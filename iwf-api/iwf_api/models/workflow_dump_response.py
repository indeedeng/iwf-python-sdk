from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkflowDumpResponse")


@attr.s(auto_attribs=True)
class WorkflowDumpResponse:
    """
    Attributes:
        checksum (str):
        total_pages (int):
        json_data (str):
    """

    checksum: str
    total_pages: int
    json_data: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        checksum = self.checksum
        total_pages = self.total_pages
        json_data = self.json_data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checksum": checksum,
                "totalPages": total_pages,
                "jsonData": json_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        checksum = d.pop("checksum")

        total_pages = d.pop("totalPages")

        json_data = d.pop("jsonData")

        workflow_dump_response = cls(
            checksum=checksum,
            total_pages=total_pages,
            json_data=json_data,
        )

        workflow_dump_response.additional_properties = d
        return workflow_dump_response

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
