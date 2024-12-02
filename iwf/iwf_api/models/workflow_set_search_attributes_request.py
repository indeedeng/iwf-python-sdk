from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_attribute import SearchAttribute


T = TypeVar("T", bound="WorkflowSetSearchAttributesRequest")


@attr.s(auto_attribs=True)
class WorkflowSetSearchAttributesRequest:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (Union[Unset, str]):
        search_attributes (Union[Unset, List['SearchAttribute']]):
    """

    workflow_id: str
    workflow_run_id: Union[Unset, str] = UNSET
    search_attributes: Union[Unset, List["SearchAttribute"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id
        workflow_run_id = self.workflow_run_id
        search_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.search_attributes, Unset):
            search_attributes = []
            for search_attributes_item_data in self.search_attributes:
                search_attributes_item = search_attributes_item_data.to_dict()

                search_attributes.append(search_attributes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id
        if search_attributes is not UNSET:
            field_dict["searchAttributes"] = search_attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.search_attribute import SearchAttribute

        d = src_dict.copy()
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId", UNSET)

        search_attributes = []
        _search_attributes = d.pop("searchAttributes", UNSET)
        for search_attributes_item_data in _search_attributes or []:
            search_attributes_item = SearchAttribute.from_dict(
                search_attributes_item_data
            )

            search_attributes.append(search_attributes_item)

        workflow_set_search_attributes_request = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            search_attributes=search_attributes,
        )

        workflow_set_search_attributes_request.additional_properties = d
        return workflow_set_search_attributes_request

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
