from typing import Any, Optional, Union

from iwf.errors import WorkflowDefinitionError
from iwf.iwf_api.models import EncodedObject
from iwf.object_encoder import ObjectEncoder


class DataAttributes:
    _type_store: dict[str, Optional[type]]
    _prefix_type_store: dict[str, Optional[type]]
    _object_encoder: ObjectEncoder
    _current_values: dict[str, Union[EncodedObject, None]]
    _updated_values_to_return: dict[str, EncodedObject]

    def __init__(
        self,
        type_store: dict[str, Optional[type]],
        prefix_type_store: dict[str, Optional[type]],
        object_encoder: ObjectEncoder,
        current_values: dict[str, Union[EncodedObject, None]],
    ):
        self._object_encoder = object_encoder
        self._type_store = type_store
        self._prefix_type_store = prefix_type_store
        self._current_values = current_values
        self._updated_values_to_return = {}

    def get_data_attribute(self, key: str) -> Any:
        is_registered, registered_type = self._validate_key_and_get_type(key)
        if not is_registered:
            raise WorkflowDefinitionError(f"data attribute %s is not registered {key}")

        encoded_object = self._current_values.get(key)
        if encoded_object is None:
            return None

        return self._object_encoder.decode(encoded_object, registered_type)

    def set_data_attribute(self, key: str, value: Any):
        is_registered, registered_type = self._validate_key_and_get_type(key)
        if not is_registered:
            raise WorkflowDefinitionError(f"data attribute %s is not registered {key}")

        if registered_type is not None and not isinstance(value, registered_type):
            raise WorkflowDefinitionError(
                f"data attribute %s is of the right type {registered_type}"
            )

        encoded_value = self._object_encoder.encode(value)
        self._current_values[key] = encoded_value
        self._updated_values_to_return[key] = encoded_value

    def get_updated_values_to_return(self) -> dict[str, EncodedObject]:
        return self._updated_values_to_return

    def _validate_key_and_get_type(self, key) -> tuple[bool, Optional[type]]:
        if key in self._type_store:
            return (True, self._type_store.get(key))

        for prefix, t in self._prefix_type_store.items():
            if key.startswith(prefix):
                return (True, t)

        return (False, None)
