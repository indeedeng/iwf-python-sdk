from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.context import Context
    from ..models.encoded_object import EncodedObject
    from ..models.key_value import KeyValue
    from ..models.search_attribute import SearchAttribute


T = TypeVar("T", bound="WorkflowStateWaitUntilRequest")


@attr.s(auto_attribs=True)
class WorkflowStateWaitUntilRequest:
    """
    Attributes:
        context (Context):
        workflow_type (str):
        workflow_state_id (str):
        state_input (Union[Unset, EncodedObject]):
        search_attributes (Union[Unset, List['SearchAttribute']]):
        data_objects (Union[Unset, List['KeyValue']]):
    """

    context: "Context"
    workflow_type: str
    workflow_state_id: str
    state_input: Union[Unset, "EncodedObject"] = UNSET
    search_attributes: Union[Unset, List["SearchAttribute"]] = UNSET
    data_objects: Union[Unset, List["KeyValue"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        context = self.context.to_dict()

        workflow_type = self.workflow_type
        workflow_state_id = self.workflow_state_id
        state_input: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.state_input, Unset):
            state_input = self.state_input.to_dict()

        search_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.search_attributes, Unset):
            search_attributes = []
            for search_attributes_item_data in self.search_attributes:
                search_attributes_item = search_attributes_item_data.to_dict()

                search_attributes.append(search_attributes_item)

        data_objects: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data_objects, Unset):
            data_objects = []
            for data_objects_item_data in self.data_objects:
                data_objects_item = data_objects_item_data.to_dict()

                data_objects.append(data_objects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "context": context,
                "workflowType": workflow_type,
                "workflowStateId": workflow_state_id,
            }
        )
        if state_input is not UNSET:
            field_dict["stateInput"] = state_input
        if search_attributes is not UNSET:
            field_dict["searchAttributes"] = search_attributes
        if data_objects is not UNSET:
            field_dict["dataObjects"] = data_objects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.context import Context
        from ..models.encoded_object import EncodedObject
        from ..models.key_value import KeyValue
        from ..models.search_attribute import SearchAttribute

        d = src_dict.copy()
        context = Context.from_dict(d.pop("context"))

        workflow_type = d.pop("workflowType")

        workflow_state_id = d.pop("workflowStateId")

        _state_input = d.pop("stateInput", UNSET)
        state_input: Union[Unset, EncodedObject]
        if isinstance(_state_input, Unset):
            state_input = UNSET
        else:
            state_input = EncodedObject.from_dict(_state_input)

        search_attributes = []
        _search_attributes = d.pop("searchAttributes", UNSET)
        for search_attributes_item_data in _search_attributes or []:
            search_attributes_item = SearchAttribute.from_dict(
                search_attributes_item_data
            )

            search_attributes.append(search_attributes_item)

        data_objects = []
        _data_objects = d.pop("dataObjects", UNSET)
        for data_objects_item_data in _data_objects or []:
            data_objects_item = KeyValue.from_dict(data_objects_item_data)

            data_objects.append(data_objects_item)

        workflow_state_wait_until_request = cls(
            context=context,
            workflow_type=workflow_type,
            workflow_state_id=workflow_state_id,
            state_input=state_input,
            search_attributes=search_attributes,
            data_objects=data_objects,
        )

        workflow_state_wait_until_request.additional_properties = d
        return workflow_state_wait_until_request

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
