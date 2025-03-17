from typing import Any, Union

from iwf.data_attributes import DataAttributes
from iwf.search_attributes import SearchAttributes


class Persistence:
    _data_attributes: DataAttributes
    _search_attributes: SearchAttributes

    def __init__(
        self,
        data_attributes: DataAttributes,
        search_attributes: SearchAttributes,
    ):
        self._data_attributes = data_attributes
        self._search_attributes = search_attributes

    def get_data_attribute(self, key: str) -> Any:
        return self._data_attributes.get_data_attribute(key)

    def set_data_attribute(self, key: str, value: Any):
        self._data_attributes.set_data_attribute(key, value)

    def get_search_attribute_int64(self, key: str) -> Union[None, int]:
        return self._search_attributes.get_search_attribute_int64(key)

    def set_search_attribute_int64(self, key: str, value: Union[None, int]):
        self._search_attributes.set_search_attribute_int64(key, value)

    def get_search_attribute_double(self, key: str) -> Union[None, float]:
        return self._search_attributes.get_search_attribute_double(key)

    def set_search_attribute_double(self, key: str, value: Union[None, float]):
        self._search_attributes.set_search_attribute_double(key, value)

    def get_search_attribute_boolean(self, key: str) -> Union[None, bool]:
        return self._search_attributes.get_search_attribute_boolean(key)

    def set_search_attribute_boolean(self, key: str, value: Union[None, bool]):
        self._search_attributes.set_search_attribute_boolean(key, value)

    def get_search_attribute_keyword(self, key: str) -> Union[None, str]:
        return self._search_attributes.get_search_attribute_keyword(key)

    def set_search_attribute_keyword(self, key: str, value: Union[None, str]):
        self._search_attributes.set_search_attribute_keyword(key, value)

    def get_search_attribute_text(self, key: str) -> Union[None, str]:
        return self._search_attributes.get_search_attribute_text(key)

    def set_search_attribute_text(self, key: str, value: Union[None, str]):
        self._search_attributes.set_search_attribute_text(key, value)

    def get_search_attribute_datetime(self, key: str) -> Union[None, str]:
        return self._search_attributes.get_search_attribute_datetime(key)

    def set_search_attribute_datetime(self, key: str, value: Union[None, str]):
        self._search_attributes.set_search_attribute_datetime(key, value)

    def get_search_attribute_keyword_array(self, key: str) -> Union[None, list[str]]:
        return self._search_attributes.get_search_attribute_keyword_array(key)

    def set_search_attribute_keyword_array(
        self, key: str, value: Union[None, list[str]]
    ):
        self._search_attributes.set_search_attribute_keyword_array(key, value)
