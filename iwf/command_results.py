import typing
from dataclasses import dataclass
from typing import Any, Union

from iwf.errors import WorkflowDefinitionError, NotRegisteredError
from iwf.iwf_api.models import (
    ChannelRequestStatus,
    CommandResults as IdlCommandResults,
    TimerStatus,
)
from iwf.iwf_api.types import Unset
from iwf.object_encoder import ObjectEncoder
from iwf.type_store import TypeStore


@dataclass
class TimerCommandResult:
    status: TimerStatus
    command_id: str


@dataclass
class InternalChannelCommandResult:
    channel_name: str
    value: Any
    status: ChannelRequestStatus
    command_id: str


@dataclass
class SignalChannelCommandResult:
    channel_name: str
    value: Any
    status: ChannelRequestStatus
    command_id: str


@dataclass
class CommandResults:
    timer_commands: list[TimerCommandResult]
    internal_channel_commands: list[InternalChannelCommandResult]
    signal_channel_commands: list[SignalChannelCommandResult]


def from_idl_command_results(
    idl_results: Union[Unset, IdlCommandResults],
    internal_channel_types: TypeStore,
    signal_channel_types: dict[str, typing.Optional[type]],
    object_encoder: ObjectEncoder,
) -> CommandResults:
    results = CommandResults(list(), list(), list())
    if isinstance(idl_results, Unset):
        return results
    if not isinstance(idl_results.timer_results, Unset):
        for timer in idl_results.timer_results:
            results.timer_commands.append(
                TimerCommandResult(timer.timer_status, timer.command_id)
            )

    if not isinstance(idl_results.inter_state_channel_results, Unset):
        for inter in idl_results.inter_state_channel_results:

            try:
                val_type = internal_channel_types.get_type(inter.channel_name)
            except NotRegisteredError as exception:
                raise WorkflowDefinitionError(
                    "internal channel is not registered: " + inter.channel_name
                ) from exception

            encoded = object_encoder.decode(inter.value, val_type)

            results.internal_channel_commands.append(
                InternalChannelCommandResult(
                    inter.channel_name,
                    encoded,
                    inter.request_status,
                    inter.command_id,
                )
            )

    if not isinstance(idl_results.signal_results, Unset):
        for sig in idl_results.signal_results:
            results.signal_channel_commands.append(
                SignalChannelCommandResult(
                    sig.signal_channel_name,
                    object_encoder.decode(
                        sig.signal_value,
                        signal_channel_types.get(sig.signal_channel_name),
                    ),
                    sig.signal_request_status,
                    sig.command_id,
                )
            )
    return results
