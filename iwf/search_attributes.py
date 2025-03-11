from typing import Any, Optional, Union

from iwf.errors import WorkflowDefinitionError
from iwf.iwf_api.models import SearchAttribute, SearchAttributeValueType

class SearchAttributes:
    _key_to_type_map = dict[str, SearchAttributeValueType]
    _int64_attribute_map: dict[str, int]
    _upsert_to_server_int64_attribute_map: dict[str, int]
    _string_attribute_map: dict[str, str]
    _upsert_to_server_string_attribute_map: dict[str, str]
    _double_attribute_map: dict[str, float]
    _upsert_to_server_double_attribute_map: dict[str, float]
    _bool_attribute_map: dict[str, bool]
    _upsert_to_server_bool_attribute_map: dict[str, bool]
    _string_array_attribute_map: dict[str, list[str]]
    _upsert_to_server_string_array_attribute_map: dict[str, list[str]]

    def __init__(
        self,
        key_to_type_map: dict[str, SearchAttributeValueType],
        search_attribute_map: Union[list[SearchAttribute], None]
    ):
        self._key_to_type_map = key_to_type_map
        self._int64_attribute_map = {}
        self._upsert_to_server_int64_attribute_map = {}
        self._string_attribute_map = {}
        self._upsert_to_server_string_attribute_map = {}
        self._double_attribute_map = {}
        self._upsert_to_server_double_attribute_map = {}
        self._bool_attribute_map = {}
        self._upsert_to_server_bool_attribute_map = {}
        self._string_array_attribute_map = {}
        self._upsert_to_server_string_array_attribute_map = {}

        if search_attribute_map is not None:
            for attribute in search_attribute_map:
                value_type = key_to_type_map[attribute.key]

                if value_type == SearchAttributeValueType.KEYWORD or value_type == SearchAttributeValueType.DATETIME or value_type == SearchAttributeValueType.TEXT:
                    self._string_attribute_map[attribute.key] = attribute.string_value
                elif value_type == SearchAttributeValueType.INT:
                    self._int64_attribute_map[attribute.key] = attribute.integer_value
                elif value_type == SearchAttributeValueType.DOUBLE:
                    self._double_attribute_map[attribute.key] = attribute.double_value
                elif value_type == SearchAttributeValueType.BOOL:
                    self._bool_attribute_map[attribute.key] = attribute.bool_value
                elif value_type == SearchAttributeValueType.KEYWORD_ARRAY:
                    self._string_array_attribute_map[attribute.key] = attribute.string_array_value
                else:
                    raise ValueError(f"empty or not supported search attribute value type, {value_type}")

    def get_search_attribute_int64(self, key: str) -> Union[int, None]:
        return self._int64_attribute_map.get(key)

    def set_search_attribute_int64(self, key: str, value: int):
        if key not in self._key_to_type_map or self._key_to_type_map[key] != SearchAttributeValueType.INT:
            raise WorkflowDefinitionError(f"key {key} is not defined as int64")
        self._int64_attribute_map[key] = value
        self._upsert_to_server_int64_attribute_map[key] = value

    def get_search_attribute_double(self, key: str) -> Union[float, None]:
        return self._double_attribute_map.get(key)

    def set_search_attribute_double(self, key: str, value: float):
        if key not in self._key_to_type_map or self._key_to_type_map[key] != SearchAttributeValueType.DOUBLE:
            raise WorkflowDefinitionError(f"key {key} is not defined as double")
        self._double_attribute_map[key] = value
        self._upsert_to_server_double_attribute_map[key] = value

    def get_search_attribute_boolean(self, key: str) -> Union[bool, None]:
        return self._bool_attribute_map.get(key)

    def set_search_attribute_boolean(self, key: str, value: bool):
        if key not in self._key_to_type_map or self._key_to_type_map[key] != SearchAttributeValueType.BOOL:
            raise WorkflowDefinitionError(f"key {key} is not defined as bool")
        self._bool_attribute_map[key] = value
        self._upsert_to_server_bool_attribute_map[key] = value

    def get_search_attribute_keyword(self, key: str) -> Union[str, None]:
        return self._string_attribute_map.get(key)

    def set_search_attribute_keyword(self, key: str, value: str):
        if key not in self._key_to_type_map or self._key_to_type_map[key] != SearchAttributeValueType.KEYWORD:
            raise WorkflowDefinitionError(f"key {key} is not defined as keyword")
        self._string_attribute_map[key] = value
        self._upsert_to_server_string_attribute_map[key] = value

    def get_search_attribute_text(self, key: str) -> Union[str, None]:
        return self._string_attribute_map.get(key)

    def set_search_attribute_text(self, key: str, value: str):
        if key not in self._key_to_type_map or self._key_to_type_map[key] != SearchAttributeValueType.TEXT:
            raise WorkflowDefinitionError(f"key {key} is not defined as text")
        self._string_attribute_map[key] = value
        self._upsert_to_server_string_attribute_map[key] = value

    def get_search_attribute_datetime(self, key: str) -> Union[str, None]:
        return self._string_attribute_map.get(key)

    def set_search_attribute_datetime(self, key: str, value: str):
        if key not in self._key_to_type_map or self._key_to_type_map[key] != SearchAttributeValueType.DATETIME:
            raise WorkflowDefinitionError(f"key {key} is not defined as datetime")
        self._string_attribute_map[key] = value
        self._upsert_to_server_string_attribute_map[key] = value

    def get_search_attribute_keyword_array(self, key: str) -> Union[list[str], None]:
        return self._string_array_attribute_map.get(key)

    def set_search_attribute_keyword_array(self, key: str, value: list[str]):
        if key not in self._key_to_type_map or self._key_to_type_map[key] != SearchAttributeValueType.KEYWORD_ARRAY:
            raise WorkflowDefinitionError(f"key {key} is not defined as keyword array")
        self._string_array_attribute_map[key] = value
        self._upsert_to_server_string_array_attribute_map[key] = value

    def get_upsert_to_server_int64_attribute_map(self) -> dict[str, int]:
        return self._upsert_to_server_int64_attribute_map

    def get_upsert_to_server_string_attribute_map(self) -> dict[str, str]:
        return self._upsert_to_server_string_attribute_map

    def get_upsert_to_server_string_array_attribute_map(self) -> dict[str, list[str]]:
        return self._upsert_to_server_string_array_attribute_map

    def get_upsert_to_server_bool_attribute_map(self) -> dict[str, bool]:
        return self._upsert_to_server_bool_attribute_map

    def get_upsert_to_server_double_attribute_map(self) -> dict[str, float]:
        return self._upsert_to_server_double_attribute_map
