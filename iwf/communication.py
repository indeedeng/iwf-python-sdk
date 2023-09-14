from typing import Any, Optional, Union

from iwf.errors import WorkflowDefinitionError
from iwf.iwf_api.models import EncodedObject, InterStateChannelPublishing
from iwf.object_encoder import ObjectEncoder
from iwf.state_movement import StateMovement


class Communication:
    _type_store: dict[str, Optional[type]]
    _object_encoder: ObjectEncoder
    _to_publish_internal_channel: dict[str, list[EncodedObject]]
    _state_movements: list[StateMovement]

    def __init__(
        self, type_store: dict[str, Optional[type]], object_encoder: ObjectEncoder
    ):
        self._object_encoder = object_encoder
        self._type_store = type_store
        self._to_publish_internal_channel = {}
        self._state_movements = []

    def trigger_state_execution(self, state: Union[str, type], state_input: Any = None):
        """

        Args:
            state: the workflowState TODO the type hint should be type[WorkflowState]
            state_input: the input of the state
        """
        movement = StateMovement.create(state, state_input)
        self._state_movements.append(movement)

    def publish_to_internal_channel(self, channel_name: str, value: Any = None):
        if channel_name not in self._type_store:
            raise WorkflowDefinitionError(
                f"InternalChannel channel_name is not defined {channel_name}"
            )

        registered_type = self._type_store.get(channel_name)
        if (
            value is not None
            and registered_type is not None
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

    def get_to_trigger_state_movements(self) -> list[StateMovement]:
        return self._state_movements
