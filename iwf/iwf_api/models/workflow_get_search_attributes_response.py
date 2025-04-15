from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_attribute import SearchAttribute


T = TypeVar("T", bound="WorkflowGetSearchAttributesResponse")


@_attrs_define
class WorkflowGetSearchAttributesResponse:
    """
    Attributes:
        search_attributes (Union[Unset, list['SearchAttribute']]):
    """

    search_attributes: Union[Unset, list["SearchAttribute"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        search_attributes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.search_attributes, Unset):
            search_attributes = []
            for search_attributes_item_data in self.search_attributes:
                search_attributes_item = search_attributes_item_data.to_dict()
                search_attributes.append(search_attributes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if search_attributes is not UNSET:
            field_dict["searchAttributes"] = search_attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_attribute import SearchAttribute

        d = dict(src_dict)
        search_attributes = []
        _search_attributes = d.pop("searchAttributes", UNSET)
        for search_attributes_item_data in _search_attributes or []:
            search_attributes_item = SearchAttribute.from_dict(search_attributes_item_data)

            search_attributes.append(search_attributes_item)

        workflow_get_search_attributes_response = cls(
            search_attributes=search_attributes,
        )

        workflow_get_search_attributes_response.additional_properties = d
        return workflow_get_search_attributes_response

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
