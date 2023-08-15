from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


class CommunicationMethodType(Enum):
    SignalChannel = 1
    InternalChannel = 2


@dataclass
class CommunicationMethod:
    name: str
    method_type: CommunicationMethodType
    value_type: Optional[type]


def signal_channel_def(name: str, value_type: type):
    return CommunicationMethod(name, CommunicationMethodType.SignalChannel, value_type)


def internal_channel_def(name: str, value_type: type):
    return CommunicationMethod(
        name, CommunicationMethodType.InternalChannel, value_type
    )


@dataclass
class CommunicationSchema:
    communication_methods: List[CommunicationMethod] = field(default_factory=list)
