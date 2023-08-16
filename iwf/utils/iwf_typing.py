from typing import TypeVar, Union

from iwf_api.types import Unset

T = TypeVar("T")


def none_type() -> type[T]:
    """
    This returns the NoneType to make it more friendly to use.
    Alternatively, users can also use Python builtin types.NoneType but mypy will complain about it.

    Returns:
        The type for None
    """
    return type(None)  # type: ignore


def check_not_unset(input: Union[Unset, T]) -> T:
    assert not isinstance(input, Unset), "instance cannot be unset"
    return T(input)
