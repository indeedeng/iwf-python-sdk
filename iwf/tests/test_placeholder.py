from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class B(ABC, Generic[T]):
    @abstractmethod
    def func1(self) -> type[T]:
        pass

    @abstractmethod
    def func2(self, t: T) -> str:
        pass

    def func3(self, t: T) -> str:
        pass


class Box(B[int]):
    def func1(self) -> type[T]:
        return int

    def func2(self, t: int) -> str:
        print(t)
        return "abc"


def test_placeholder() -> None:
    box1 = Box()
    print(box1.func1())
    print(box1.func2(123))

    print(box1.func3(456))
