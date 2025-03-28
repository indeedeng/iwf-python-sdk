from typing import Any, Union

from iwf.errors import WorkflowDefinitionError
from iwf.iwf_api.models import EncodedObject
from iwf.object_encoder import ObjectEncoder
from iwf.type_store import TypeStore


class DataAttributes:
    _type_store: TypeStore
    _object_encoder: ObjectEncoder
    _current_values: dict[str, Union[EncodedObject, None]]
    _updated_values_to_return: dict[str, EncodedObject]

    def __init__(
        self,
        type_store: TypeStore,
        object_encoder: ObjectEncoder,
        current_values: dict[str, Union[EncodedObject, None]],
    ):
        self._object_encoder = object_encoder
        self._type_store = type_store
        self._current_values = current_values
        self._updated_values_to_return = {}

    def get_data_attribute(self, key: str) -> Any:
        is_registered = self._type_store.is_valid_name_or_prefix(key)
        if not is_registered:
            raise WorkflowDefinitionError(f"data attribute %s is not registered {key}")

        encoded_object = self._current_values.get(key)
        if encoded_object is None:
            return None

        registered_type = self._type_store.get_type(key)
        return self._object_encoder.decode(encoded_object, registered_type)

    def set_data_attribute(self, key: str, value: Any):
        is_registered = self._type_store.is_valid_name_or_prefix(key)
        if not is_registered:
            raise WorkflowDefinitionError(f"data attribute %s is not registered {key}")

        registered_type = self._type_store.get_type(key)
        if registered_type is not None and not isinstance(value, registered_type):
            raise WorkflowDefinitionError(
                f"data attribute %s is of the right type {registered_type}"
            )

        encoded_value = self._object_encoder.encode(value)
        self._current_values[key] = encoded_value
        self._updated_values_to_return[key] = encoded_value

    def get_updated_values_to_return(self) -> dict[str, EncodedObject]:
        return self._updated_values_to_return
