from dataclasses import dataclass
from typing import Optional

from iwf.iwf_api.models.search_attribute import SearchAttribute
from iwf.iwf_api.models.search_attribute_value_type import SearchAttributeValueType


@dataclass
class SearchAttributeState:
    key: str
    sa_type: SearchAttributeValueType
    search_attribute: Optional[SearchAttribute]


@dataclass
class SearchAttributePrefixState:
    key: str
    sa_type: SearchAttributeValueType
    search_attributes: dict[str, SearchAttribute]
