from dataclasses import dataclass
from typing import Any, Union

from iwf_api.models import (
    ChannelRequestStatus,
    CommandResults as IdlCommandResults,
    TimerStatus,
)
from iwf_api.types import Unset

from iwf.object_encoder import ObjectEncoder
from iwf.registry import TypeStore


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
class CommandResults:
    timer_commands: list[TimerCommandResult]
    internal_channel_commands: list[InternalChannelCommandResult]


def from_idl_command_results(
    idl_results: Union[Unset, IdlCommandResults],
    internal_channel_types: TypeStore,
    object_encoder: ObjectEncoder,
) -> CommandResults:
    results = CommandResults(list(), list())
    if isinstance(idl_results, Unset):
        return results
    if not isinstance(idl_results.timer_results, Unset):
        for timer in idl_results.timer_results:
            results.timer_commands.append(
                TimerCommandResult(timer.timer_status, timer.command_id)
            )

    if not isinstance(idl_results.inter_state_channel_results, Unset):
        for inter in idl_results.inter_state_channel_results:
            results.internal_channel_commands.append(
                InternalChannelCommandResult(
                    inter.channel_name,
                    object_encoder.decode(
                        inter.value, internal_channel_types.get(inter.channel_name)
                    ),
                    inter.request_status,
                    inter.command_id,
                )
            )
    return results
