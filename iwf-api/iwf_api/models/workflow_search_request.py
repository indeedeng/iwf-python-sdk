from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowSearchRequest")


@attr.s(auto_attribs=True)
class WorkflowSearchRequest:
    """
    Attributes:
        query (str):
        page_size (Union[Unset, int]):
        next_page_token (Union[Unset, str]):
    """

    query: str
    page_size: Union[Unset, int] = UNSET
    next_page_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query = self.query
        page_size = self.page_size
        next_page_token = self.next_page_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if page_size is not UNSET:
            field_dict["pageSize"] = page_size
        if next_page_token is not UNSET:
            field_dict["nextPageToken"] = next_page_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query = d.pop("query")

        page_size = d.pop("pageSize", UNSET)

        next_page_token = d.pop("nextPageToken", UNSET)

        workflow_search_request = cls(
            query=query,
            page_size=page_size,
            next_page_token=next_page_token,
        )

        workflow_search_request.additional_properties = d
        return workflow_search_request

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
