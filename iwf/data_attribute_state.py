from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DataAttributeState:
    key: str
    da_type: Optional[type]
    data_attribute: Any


@dataclass
class DataAttributePrefixState:
    prefix: str
    da_type: Optional[type]
    data_attribute: list[DataAttributeState]
