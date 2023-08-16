from typing import TypeVar, Optional, Union

from iwf_api.types import Unset

T = TypeVar("T")


def union_to_optional(input: Union[Unset, T]) -> Optional[T]:
    if input is Unset:
        return None
    else:
        return input  # type: ignore


def none_type() -> type[T]:
    """
    This returns the NoneType to make it more friendly to use.
    Alternatively, users can also use Python builtin types.NoneType but mypy will complain about it.

    Returns:
        The type for None
    """
    return type(None)  # type: ignore
