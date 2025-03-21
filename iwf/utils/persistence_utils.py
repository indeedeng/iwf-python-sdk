from iwf.iwf_api.models import SearchAttributeValueType, SearchAttribute
from iwf.utils.iwf_typing import unset_to_none


def get_search_attribute_value(
    sa_type: SearchAttributeValueType, attribute: SearchAttribute
):
    if (
        sa_type == SearchAttributeValueType.KEYWORD
        or sa_type == SearchAttributeValueType.DATETIME
        or sa_type == SearchAttributeValueType.TEXT
    ):
        return unset_to_none(attribute.string_value)
    elif sa_type == SearchAttributeValueType.INT:
        return unset_to_none(attribute.integer_value)
    elif sa_type == SearchAttributeValueType.DOUBLE:
        return unset_to_none(attribute.double_value)
    elif sa_type == SearchAttributeValueType.BOOL:
        return unset_to_none(attribute.bool_value)
    elif sa_type == SearchAttributeValueType.KEYWORD_ARRAY:
        return unset_to_none(attribute.string_array_value)
    else:
        raise ValueError(f"not supported search attribute value type, {sa_type}")
