from typing import Optional, TypeVar, Union

from iwf.iwf_api.types import Unset

T = TypeVar("T")


def unset_to_none(input: Union[Unset, T]) -> Optional[T]:
    if isinstance(input, Unset):
        return None
    return input


def assert_not_unset(input: Union[Unset, T]) -> T:
    if isinstance(input, Unset):
        raise RuntimeError("the value shouldn't be Unset")
    return input
