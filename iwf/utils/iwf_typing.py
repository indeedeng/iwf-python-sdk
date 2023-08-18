from typing import TypeVar, Union, Optional

from iwf_api.types import Unset

T = TypeVar("T")


NoneType: type = type(None)


def unset_to_none(input: Union[Unset, T]) -> Optional[T]:
    if isinstance(input, Unset):
        return None
    return input
