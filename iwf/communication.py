from typing import Any, Optional, Union

from iwf.errors import WorkflowDefinitionError
from iwf.iwf_api.models import (
    EncodedObject,
    InterStateChannelPublishing,
    WorkflowWorkerRpcRequestInternalChannelInfos,
    WorkflowWorkerRpcRequestSignalChannelInfos,
)
from iwf.object_encoder import ObjectEncoder
from iwf.state_movement import StateMovement


class Communication:
    _internal_channel_type_store: dict[str, Optional[type]]
    _signal_channel_type_store: dict[str, Optional[type]]
    _object_encoder: ObjectEncoder
    _to_publish_internal_channel: dict[str, list[EncodedObject]]
    _state_movements: list[StateMovement]
    _internal_channel_infos: Optional[WorkflowWorkerRpcRequestInternalChannelInfos]
    _signal_channel_infos: Optional[WorkflowWorkerRpcRequestSignalChannelInfos]

    def __init__(
        self,
        internal_channel_type_store: dict[str, Optional[type]],
        signal_channel_type_store: dict[str, Optional[type]],
        object_encoder: ObjectEncoder,
        internal_channel_infos: Optional[WorkflowWorkerRpcRequestInternalChannelInfos],
        signal_channel_infos: Optional[WorkflowWorkerRpcRequestSignalChannelInfos],
    ):
        self._object_encoder = object_encoder
        self._internal_channel_type_store = internal_channel_type_store
        self._signal_channel_type_store = signal_channel_type_store
        self._to_publish_internal_channel = {}
        self._state_movements = []
        self._internal_channel_infos = internal_channel_infos
        self._signal_channel_infos = signal_channel_infos

    def trigger_state_execution(self, state: Union[str, type], state_input: Any = None):
        """

        Args:
            state: the workflowState TODO the type hint should be type[WorkflowState]
            state_input: the input of the state
        """
        movement = StateMovement.create(state, state_input)
        self._state_movements.append(movement)

    def publish_to_internal_channel(self, channel_name: str, value: Any = None):
        registered_type = self._internal_channel_type_store.get(channel_name)

        if registered_type is None:
            for name, t in self._internal_channel_type_store.items():
                if channel_name.startswith(name):
                    registered_type = t

        if registered_type is None:
            raise WorkflowDefinitionError(
                f"InternalChannel channel_name is not defined {channel_name}"
            )

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

    def get_internal_channel_size(self, channel_name):
        registered_type = self._internal_channel_type_store.get(channel_name)

        if registered_type is None:
            for name, t in self._internal_channel_type_store.items():
                if channel_name.startswith(name):
                    registered_type = t

        if registered_type is None:
            raise WorkflowDefinitionError(
                f"InternalChannel channel_name is not defined {channel_name}"
            )

        if (
            self._internal_channel_infos is not None
            and channel_name in self._internal_channel_infos
        ):
            server_channel_size = self._internal_channel_infos[channel_name].size
        else:
            server_channel_size = 0

        if channel_name in self._to_publish_internal_channel:
            buffer_channel_size = len(self._to_publish_internal_channel[channel_name])
        else:
            buffer_channel_size = 0

        return server_channel_size + buffer_channel_size

    def get_signal_channel_size(self, channel_name):
        registered_type = self._signal_channel_type_store.get(channel_name)

        if registered_type is None:
            for name, t in self._signal_channel_type_store.items():
                if channel_name.startswith(name):
                    registered_type = t

        if registered_type is None:
            raise WorkflowDefinitionError(
                f"SignalChannel channel_name is not defined {channel_name}"
            )

        if (
            self._signal_channel_infos is not None
            and channel_name in self._signal_channel_infos
        ):
            return self._signal_channel_infos[channel_name].size
        else:
            return 0
