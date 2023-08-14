from dataclasses import dataclass
from enum import Enum

from iwf_api.models import SearchAttributeValueType


class PersistenceFieldType(Enum):
    DataAttribute = 1
    SearchAttribute = 2


@dataclass
class PersistenceField:
    key: str
    field_type: PersistenceFieldType
    search_attribute_type: SearchAttributeValueType


@dataclass
class PersistenceSchema:
    persistence_fields: [PersistenceField]
