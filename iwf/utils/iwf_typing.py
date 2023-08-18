from typing import TypeVar, Union, Optional

from iwf_api.types import Unset

T = TypeVar("T")


def none_type() -> type[T]:
    """
    This returns the NoneType to make it more friendly to use.
    Alternatively, users can also use Python builtin types.NoneType but mypy will complain about it.

    NOTE: this only works for Python 3.9 and above
    Returns:
        The type for None
    """
    return type(None)  # type: ignore


def check_not_unset(input: Union[Unset, T]) -> T:
    assert not isinstance(input, Unset), "instance cannot be unset"
    return input


def unset_to_none(input: Union[Unset, T]) -> Optional[T]:
    if isinstance(input, Unset):
        return None
    return input
