from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List

from iwf_api.models import SearchAttributeValueType


class PersistenceFieldType(Enum):
    DataAttribute = 1
    SearchAttribute = 2


@dataclass
class PersistenceField:
    key: str
    field_type: PersistenceFieldType
    search_attribute_type: Optional[SearchAttributeValueType] = None


def data_attribute_def(key: str) -> PersistenceField:
    return PersistenceField(key, PersistenceFieldType.DataAttribute)


def search_attribute_def(
    key: str, sa_type: SearchAttributeValueType
) -> PersistenceField:
    return PersistenceField(key, PersistenceFieldType.SearchAttribute, sa_type)


@dataclass
class PersistenceSchema:
    persistence_fields: List[PersistenceField] = field(default_factory=list)
