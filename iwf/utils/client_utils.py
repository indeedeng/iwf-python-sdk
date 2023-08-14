from typing import Any

from iwf_api.models import SearchAttribute, SearchAttributeValueType


def get_search_attribute_value(
    search_attribute_value_type: SearchAttributeValueType,
    search_attribute: SearchAttribute,
) -> Any:
    match search_attribute_value_type:
        case SearchAttributeValueType.INT:
            return search_attribute.integer_value
        case SearchAttributeValueType.DOUBLE:
            return search_attribute.double_value
        case SearchAttributeValueType.BOOL:
            return search_attribute.bool_value
        case SearchAttributeValueType.KEYWORD | SearchAttributeValueType.TEXT | SearchAttributeValueType.DATETIME:
            return search_attribute.string_value
        case SearchAttributeValueType.KEYWORD_ARRAY:
            return search_attribute.string_array_value
        case _:
            raise ValueError(
                f"Unknown search attribute value type: {search_attribute_value_type}",
            )
