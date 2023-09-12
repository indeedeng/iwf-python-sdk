import time
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional, Union

from iwf_api.models import CommandWaitingType
from iwf_api.models.command_request import CommandRequest as IdlCommandRequest
from iwf_api.models.inter_state_channel_command import (
    InterStateChannelCommand as IdlInternalChannelCommand,
)
from iwf_api.models.signal_command import SignalCommand as IdlSignalCommand
from iwf_api.models.timer_command import TimerCommand as IdlTimerCommand


@dataclass
class TimerCommand:
    command_id: str
    firing_unix_timestamp_seconds: int

    @classmethod
    def timer_command_by_duration(
        cls, duration: timedelta, command_id: Optional[str] = None
    ):
        return TimerCommand(
            command_id if command_id is not None else "",
            int(time.time()) + int(duration.total_seconds()),
        )


@dataclass
class InternalChannelCommand:
    command_id: str
    channel_name: str

    @classmethod
    def by_name(cls, channel_name: str, command_id: Optional[str] = None):
        return InternalChannelCommand(
            command_id if command_id is not None else "", channel_name
        )


@dataclass
class SignalChannelCommand:
    command_id: str
    channel_name: str

    @classmethod
    def by_name(cls, channel_name: str, command_id: Optional[str] = None):
        return SignalChannelCommand(
            command_id if command_id is not None else "", channel_name
        )


BaseCommand = Union[TimerCommand, InternalChannelCommand]


@dataclass
class CommandRequest:
    commands: list[BaseCommand]
    command_waiting_type: CommandWaitingType

    @classmethod
    def for_any_command_completed(cls, *commands: BaseCommand):
        bc = [c for c in commands]
        return CommandRequest(bc, CommandWaitingType.ANY_COMPLETED)

    @classmethod
    def for_all_command_completed(cls, *commands: BaseCommand):
        bc = [c for c in commands]
        return CommandRequest(bc, CommandWaitingType.ALL_COMPLETED)

    @classmethod
    def empty(cls):
        return CommandRequest(list(), CommandWaitingType.ALL_COMPLETED)


def _to_idl_command_request(request: CommandRequest) -> IdlCommandRequest:
    req = IdlCommandRequest(
        command_waiting_type=request.command_waiting_type,
    )

    timer_commands = [
        IdlTimerCommand(t.command_id, t.firing_unix_timestamp_seconds)
        for t in request.commands
        if isinstance(t, TimerCommand)
    ]

    internal_channel_commands = [
        IdlInternalChannelCommand(i.command_id, i.channel_name)
        for i in request.commands
        if isinstance(i, InternalChannelCommand)
    ]

    signal_commands = [
        IdlSignalCommand(i.command_id, i.channel_name)
        for i in request.commands
        if isinstance(i, SignalChannelCommand)
    ]

    if len(timer_commands) > 0:
        req.timer_commands = timer_commands
    if len(internal_channel_commands) > 0:
        req.inter_state_channel_commands = internal_channel_commands
    if len(signal_commands) > 0:
        req.signal_commands = signal_commands
    return req
