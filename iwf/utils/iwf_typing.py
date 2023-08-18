from typing import TypeVar, Union, Optional

from iwf_api.types import Unset

T = TypeVar("T")


NoneType: type = type(None)


def check_not_unset(input: Union[Unset, T]) -> T:
    assert not isinstance(input, Unset), "instance cannot be unset"
    return input


def unset_to_none(input: Union[Unset, T]) -> Optional[T]:
    if isinstance(input, Unset):
        return None
    return input
