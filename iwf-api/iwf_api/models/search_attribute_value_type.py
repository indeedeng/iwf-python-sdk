from enum import Enum


class SearchAttributeValueType(str, Enum):
    BOOL = "BOOL"
    DATETIME = "DATETIME"
    DOUBLE = "DOUBLE"
    INT = "INT"
    KEYWORD = "KEYWORD"
    KEYWORD_ARRAY = "KEYWORD_ARRAY"
    TEXT = "TEXT"

    def __str__(self) -> str:
        return str(self.value)
