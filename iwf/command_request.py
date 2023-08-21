import time
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from iwf_api.models import CommandWaitingType
from iwf_api.models.command_request import CommandRequest as IdlCommandRequest


@dataclass
class TimerCommand:
    command_id: Optional[str]
    firing_unix_timestamp_seconds: int

    @classmethod
    def timer_command_by_duration(
        cls, duration: timedelta, command_id: Optional[str] = None
    ):
        return TimerCommand(
            command_id, int(time.time()) + int(duration.total_seconds())
        )


@dataclass
class CommandRequest:
    pass


def _to_idl_command_request(request: CommandRequest) -> IdlCommandRequest:
    # TODO
    return IdlCommandRequest(command_waiting_type=CommandWaitingType.ALL_COMPLETED)
