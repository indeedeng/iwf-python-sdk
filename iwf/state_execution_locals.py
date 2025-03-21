from typing import Any, List, Tuple

from iwf.errors import WorkflowDefinitionError
from iwf.iwf_api.models import EncodedObject, KeyValue
from iwf.object_encoder import ObjectEncoder


class StateExecutionLocals:
    _record_events: dict[str, EncodedObject]
    _attribute_name_to_encoded_object_map: dict[str, EncodedObject]
    _upsert_attributes_to_return_to_server: dict[str, EncodedObject]
    _object_encoder: ObjectEncoder

    def __init__(
        self,
        attribute_name_to_encoded_object_map: dict[str, EncodedObject],
        object_encoder: ObjectEncoder,
    ):
        self._object_encoder = object_encoder
        self._attribute_name_to_encoded_object_map = (
            attribute_name_to_encoded_object_map
        )
        self._upsert_attributes_to_return_to_server = {}
        self._record_events = {}

    def set_state_execution_local(self, key: str, value: Any):
        encoded_data = self._object_encoder.encode(value)
        self._attribute_name_to_encoded_object_map[key] = encoded_data
        self._upsert_attributes_to_return_to_server[key] = encoded_data

    def get_state_execution_local(self, key: str) -> Any:
        encoded_object = self._attribute_name_to_encoded_object_map.get(key)
        if encoded_object is None:
            return None
        return self._object_encoder.decode(encoded_object)

    def record_event(self, key: str, *event_data: Tuple[Any, ...]):
        if key in self._record_events:
            raise WorkflowDefinitionError("Cannot record the same event more than once")

        if event_data is not None and len(event_data) == 1:
            self._record_events[key] = self._object_encoder.encode(event_data[0])

        self._record_events[key] = self._object_encoder.encode(event_data)

    def get_upsert_state_execution_local_attributes(self) -> List[KeyValue]:
        return [
            KeyValue(item_key, item_value)
            for item_key, item_value in self._upsert_attributes_to_return_to_server.items()
        ]

    def get_record_events(self) -> List[KeyValue]:
        return [
            KeyValue(item_key, item_value)
            for item_key, item_value in self._record_events.items()
        ]
