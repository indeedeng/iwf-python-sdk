from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.command_request import CommandRequest
    from ..models.inter_state_channel_publishing import InterStateChannelPublishing
    from ..models.key_value import KeyValue
    from ..models.search_attribute import SearchAttribute


T = TypeVar("T", bound="WorkflowStateWaitUntilResponse")


@_attrs_define
class WorkflowStateWaitUntilResponse:
    """
    Attributes:
        local_activity_input (Union[Unset, str]):
        upsert_search_attributes (Union[Unset, list['SearchAttribute']]):
        upsert_data_objects (Union[Unset, list['KeyValue']]):
        command_request (Union[Unset, CommandRequest]):
        upsert_state_locals (Union[Unset, list['KeyValue']]):
        record_events (Union[Unset, list['KeyValue']]):
        publish_to_inter_state_channel (Union[Unset, list['InterStateChannelPublishing']]):
    """

    local_activity_input: Union[Unset, str] = UNSET
    upsert_search_attributes: Union[Unset, list["SearchAttribute"]] = UNSET
    upsert_data_objects: Union[Unset, list["KeyValue"]] = UNSET
    command_request: Union[Unset, "CommandRequest"] = UNSET
    upsert_state_locals: Union[Unset, list["KeyValue"]] = UNSET
    record_events: Union[Unset, list["KeyValue"]] = UNSET
    publish_to_inter_state_channel: Union[Unset, list["InterStateChannelPublishing"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        local_activity_input = self.local_activity_input

        upsert_search_attributes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.upsert_search_attributes, Unset):
            upsert_search_attributes = []
            for upsert_search_attributes_item_data in self.upsert_search_attributes:
                upsert_search_attributes_item = upsert_search_attributes_item_data.to_dict()
                upsert_search_attributes.append(upsert_search_attributes_item)

        upsert_data_objects: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.upsert_data_objects, Unset):
            upsert_data_objects = []
            for upsert_data_objects_item_data in self.upsert_data_objects:
                upsert_data_objects_item = upsert_data_objects_item_data.to_dict()
                upsert_data_objects.append(upsert_data_objects_item)

        command_request: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.command_request, Unset):
            command_request = self.command_request.to_dict()

        upsert_state_locals: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.upsert_state_locals, Unset):
            upsert_state_locals = []
            for upsert_state_locals_item_data in self.upsert_state_locals:
                upsert_state_locals_item = upsert_state_locals_item_data.to_dict()
                upsert_state_locals.append(upsert_state_locals_item)

        record_events: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.record_events, Unset):
            record_events = []
            for record_events_item_data in self.record_events:
                record_events_item = record_events_item_data.to_dict()
                record_events.append(record_events_item)

        publish_to_inter_state_channel: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.publish_to_inter_state_channel, Unset):
            publish_to_inter_state_channel = []
            for publish_to_inter_state_channel_item_data in self.publish_to_inter_state_channel:
                publish_to_inter_state_channel_item = publish_to_inter_state_channel_item_data.to_dict()
                publish_to_inter_state_channel.append(publish_to_inter_state_channel_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if local_activity_input is not UNSET:
            field_dict["localActivityInput"] = local_activity_input
        if upsert_search_attributes is not UNSET:
            field_dict["upsertSearchAttributes"] = upsert_search_attributes
        if upsert_data_objects is not UNSET:
            field_dict["upsertDataObjects"] = upsert_data_objects
        if command_request is not UNSET:
            field_dict["commandRequest"] = command_request
        if upsert_state_locals is not UNSET:
            field_dict["upsertStateLocals"] = upsert_state_locals
        if record_events is not UNSET:
            field_dict["recordEvents"] = record_events
        if publish_to_inter_state_channel is not UNSET:
            field_dict["publishToInterStateChannel"] = publish_to_inter_state_channel

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.command_request import CommandRequest
        from ..models.inter_state_channel_publishing import InterStateChannelPublishing
        from ..models.key_value import KeyValue
        from ..models.search_attribute import SearchAttribute

        d = dict(src_dict)
        local_activity_input = d.pop("localActivityInput", UNSET)

        upsert_search_attributes = []
        _upsert_search_attributes = d.pop("upsertSearchAttributes", UNSET)
        for upsert_search_attributes_item_data in _upsert_search_attributes or []:
            upsert_search_attributes_item = SearchAttribute.from_dict(upsert_search_attributes_item_data)

            upsert_search_attributes.append(upsert_search_attributes_item)

        upsert_data_objects = []
        _upsert_data_objects = d.pop("upsertDataObjects", UNSET)
        for upsert_data_objects_item_data in _upsert_data_objects or []:
            upsert_data_objects_item = KeyValue.from_dict(upsert_data_objects_item_data)

            upsert_data_objects.append(upsert_data_objects_item)

        _command_request = d.pop("commandRequest", UNSET)
        command_request: Union[Unset, CommandRequest]
        if isinstance(_command_request, Unset):
            command_request = UNSET
        else:
            command_request = CommandRequest.from_dict(_command_request)

        upsert_state_locals = []
        _upsert_state_locals = d.pop("upsertStateLocals", UNSET)
        for upsert_state_locals_item_data in _upsert_state_locals or []:
            upsert_state_locals_item = KeyValue.from_dict(upsert_state_locals_item_data)

            upsert_state_locals.append(upsert_state_locals_item)

        record_events = []
        _record_events = d.pop("recordEvents", UNSET)
        for record_events_item_data in _record_events or []:
            record_events_item = KeyValue.from_dict(record_events_item_data)

            record_events.append(record_events_item)

        publish_to_inter_state_channel = []
        _publish_to_inter_state_channel = d.pop("publishToInterStateChannel", UNSET)
        for publish_to_inter_state_channel_item_data in _publish_to_inter_state_channel or []:
            publish_to_inter_state_channel_item = InterStateChannelPublishing.from_dict(
                publish_to_inter_state_channel_item_data
            )

            publish_to_inter_state_channel.append(publish_to_inter_state_channel_item)

        workflow_state_wait_until_response = cls(
            local_activity_input=local_activity_input,
            upsert_search_attributes=upsert_search_attributes,
            upsert_data_objects=upsert_data_objects,
            command_request=command_request,
            upsert_state_locals=upsert_state_locals,
            record_events=record_events,
            publish_to_inter_state_channel=publish_to_inter_state_channel,
        )

        workflow_state_wait_until_response.additional_properties = d
        return workflow_state_wait_until_response

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
