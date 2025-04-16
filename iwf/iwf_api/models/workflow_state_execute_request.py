from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.command_results import CommandResults
    from ..models.context import Context
    from ..models.encoded_object import EncodedObject
    from ..models.key_value import KeyValue
    from ..models.search_attribute import SearchAttribute


T = TypeVar("T", bound="WorkflowStateExecuteRequest")


@_attrs_define
class WorkflowStateExecuteRequest:
    """
    Attributes:
        context (Context):
        workflow_type (str):
        workflow_state_id (str):
        state_input (Union[Unset, EncodedObject]):
        search_attributes (Union[Unset, list['SearchAttribute']]):
        data_objects (Union[Unset, list['KeyValue']]):
        state_locals (Union[Unset, list['KeyValue']]):
        command_results (Union[Unset, CommandResults]):
    """

    context: "Context"
    workflow_type: str
    workflow_state_id: str
    state_input: Union[Unset, "EncodedObject"] = UNSET
    search_attributes: Union[Unset, list["SearchAttribute"]] = UNSET
    data_objects: Union[Unset, list["KeyValue"]] = UNSET
    state_locals: Union[Unset, list["KeyValue"]] = UNSET
    command_results: Union[Unset, "CommandResults"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context = self.context.to_dict()

        workflow_type = self.workflow_type

        workflow_state_id = self.workflow_state_id

        state_input: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.state_input, Unset):
            state_input = self.state_input.to_dict()

        search_attributes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.search_attributes, Unset):
            search_attributes = []
            for search_attributes_item_data in self.search_attributes:
                search_attributes_item = search_attributes_item_data.to_dict()
                search_attributes.append(search_attributes_item)

        data_objects: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data_objects, Unset):
            data_objects = []
            for data_objects_item_data in self.data_objects:
                data_objects_item = data_objects_item_data.to_dict()
                data_objects.append(data_objects_item)

        state_locals: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.state_locals, Unset):
            state_locals = []
            for state_locals_item_data in self.state_locals:
                state_locals_item = state_locals_item_data.to_dict()
                state_locals.append(state_locals_item)

        command_results: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.command_results, Unset):
            command_results = self.command_results.to_dict()

        field_dict: dict[str, Any] = {}
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
            field_dict["DataObjects"] = data_objects
        if state_locals is not UNSET:
            field_dict["stateLocals"] = state_locals
        if command_results is not UNSET:
            field_dict["commandResults"] = command_results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.command_results import CommandResults
        from ..models.context import Context
        from ..models.encoded_object import EncodedObject
        from ..models.key_value import KeyValue
        from ..models.search_attribute import SearchAttribute

        d = dict(src_dict)
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
            search_attributes_item = SearchAttribute.from_dict(search_attributes_item_data)

            search_attributes.append(search_attributes_item)

        data_objects = []
        _data_objects = d.pop("DataObjects", UNSET)
        for data_objects_item_data in _data_objects or []:
            data_objects_item = KeyValue.from_dict(data_objects_item_data)

            data_objects.append(data_objects_item)

        state_locals = []
        _state_locals = d.pop("stateLocals", UNSET)
        for state_locals_item_data in _state_locals or []:
            state_locals_item = KeyValue.from_dict(state_locals_item_data)

            state_locals.append(state_locals_item)

        _command_results = d.pop("commandResults", UNSET)
        command_results: Union[Unset, CommandResults]
        if isinstance(_command_results, Unset):
            command_results = UNSET
        else:
            command_results = CommandResults.from_dict(_command_results)

        workflow_state_execute_request = cls(
            context=context,
            workflow_type=workflow_type,
            workflow_state_id=workflow_state_id,
            state_input=state_input,
            search_attributes=search_attributes,
            data_objects=data_objects,
            state_locals=state_locals,
            command_results=command_results,
        )

        workflow_state_execute_request.additional_properties = d
        return workflow_state_execute_request

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
