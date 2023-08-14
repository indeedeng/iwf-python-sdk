from dataclasses import dataclass
from enum import Enum


class CommunicationMethodType(Enum):
    SignalChannel = 1
    InternalChannel = 2


@dataclass
class CommunicationMethod:
    name: str
    method_type: CommunicationMethodType


@dataclass
class CommunicationSchema:
    communication_methods: [CommunicationMethod]
