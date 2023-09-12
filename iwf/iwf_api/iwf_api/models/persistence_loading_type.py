from enum import Enum


class PersistenceLoadingType(str, Enum):
    LOAD_ALL_WITHOUT_LOCKING = "LOAD_ALL_WITHOUT_LOCKING"
    LOAD_NONE = "LOAD_NONE"
    LOAD_PARTIAL_WITHOUT_LOCKING = "LOAD_PARTIAL_WITHOUT_LOCKING"
    LOAD_PARTIAL_WITH_EXCLUSIVE_LOCK = "LOAD_PARTIAL_WITH_EXCLUSIVE_LOCK"

    def __str__(self) -> str:
        return str(self.value)
