from typing import Optional
from enum import Enum

from iwf.communication_schema import CommunicationMethod
from iwf.errors import WorkflowDefinitionError, NotRegisteredError


class Type(Enum):
    INTERNAL_CHANNEL = 1
    # TODO: extend to other types
    # DATA_ATTRIBUTE = 2
    # SIGNAL_CHANNEL = 3


class TypeStore:
    _class_type: Type
    _name_to_type_store: dict[str, Optional[type]]
    _prefix_to_type_store: dict[str, Optional[type]]

    def __init__(self, class_type: Type):
        self._class_type = class_type
        self._name_to_type_store = dict()
        self._prefix_to_type_store = dict()

    def is_valid_name_or_prefix(self, name: str) -> bool:
        t = self._do_get_type(name)
        return t is not None

    def get_type(self, name: str) -> type:
        t = self._do_get_type(name)

        if t is None:
            raise NotRegisteredError(f"{self._class_type} not registered: {name}")

        return t

    def add_internal_channel_def(self, obj: CommunicationMethod):
        if self._class_type != Type.INTERNAL_CHANNEL:
            raise ValueError(
                f"Cannot add internal channel definition to {self._class_type}"
            )
        self._do_add_to_store(obj.is_prefix, obj.name, obj.value_type)

    def _do_get_type(self, name: str) -> Optional[type]:
        if name in self._name_to_type_store:
            return self._name_to_type_store[name]

        prefixes = self._prefix_to_type_store.keys()

        first = next((prefix for prefix in prefixes if name.startswith(prefix)), None)

        if first is None:
            return None

        return self._prefix_to_type_store.get(first, None)

    def _do_add_to_store(self, is_prefix: bool, name: str, t: Optional[type]):
        if is_prefix:
            store = self._prefix_to_type_store
        else:
            store = self._name_to_type_store

        if name in store:
            raise WorkflowDefinitionError(
                f"{self._class_type} name/prefix {name} already exists"
            )

        store[name] = t
