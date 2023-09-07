from typing import Any

from iwf_api.models import EncodedObject, InterStateChannelPublishing

from iwf.errors import WorkflowDefinitionError
from iwf.object_encoder import ObjectEncoder
from iwf.registry import TypeStore


class Communication:
    _type_store: TypeStore
    _object_encoder: ObjectEncoder
    _to_publish_internal_channel: dict[str, list[EncodedObject]]

    def publish_to_internal_channel(self, channel_name: str, value: Any):
        registered_type = self._type_store[channel_name]
        if (
            value is not None
            and type is not None
            and not isinstance(value, registered_type)
        ):
            raise WorkflowDefinitionError(
                f"InternalChannel value is not of type {registered_type}"
            )
        vals = self._to_publish_internal_channel.get(channel_name)
        if vals is None:
            vals = []
        vals.append(self._object_encoder.encode(value))
        self._to_publish_internal_channel[channel_name] = vals

    def get_to_publishing_internal_channel(self) -> list[InterStateChannelPublishing]:
        pubs = []
        for name, vals in self._to_publish_internal_channel.items():
            for val in vals:
                pubs.append(InterStateChannelPublishing(name, val))
        return pubs
