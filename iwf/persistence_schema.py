from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from iwf.iwf_api.models import SearchAttributeValueType


class PersistenceFieldType(Enum):
    DataAttribute = 1
    SearchAttribute = 2
    DataAttributePrefix = 3


@dataclass
class PersistenceField:
    key: str
    field_type: PersistenceFieldType
    value_type: Optional[type]
    search_attribute_type: Optional[SearchAttributeValueType] = None

    @classmethod
    def data_attribute_def(cls, key: str, value_type: Optional[type]):
        return PersistenceField(key, PersistenceFieldType.DataAttribute, value_type)

    @classmethod
    def search_attribute_def(cls, key: str, sa_type: SearchAttributeValueType):
        return PersistenceField(
            key, PersistenceFieldType.SearchAttribute, None, sa_type
        )

    @classmethod
    def data_attribute_prefix_def(cls, key: str, value_type: Optional[type]):
        return PersistenceField(
            key, PersistenceFieldType.DataAttributePrefix, value_type
        )


@dataclass
class PersistenceSchema:
    persistence_fields: List[PersistenceField] = field(default_factory=list)

    @classmethod
    def create(cls, *args: PersistenceField):
        return PersistenceSchema(list(args))
