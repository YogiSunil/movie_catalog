from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, Generic, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _Node(Generic[K, V]):
    key: K
    value: V
    left: Optional["_Node[K, V]"] = None
    right: Optional["_Node[K, V]"] = None
    height: int = 1


class AVLTreeMap(Generic[K, V]):
    def __init__(self) -> None:
        self._root: Optional[_Node[K, V]] = None
        self._size = 0

    def set(self, key: K, value: V) -> None:
        raise NotImplementedError

    def get(self, key: K) -> Optional[V]:
        raise NotImplementedError

    def delete(self, key: K) -> bool:
        raise NotImplementedError

    def items(self) -> Generator[tuple[K, V], None, None]:
        raise NotImplementedError

    def range(self, low: K, high: K) -> Generator[tuple[K, V], None, None]:
        raise NotImplementedError

    def height(self) -> int:
        return 0

    def __len__(self) -> int:
        return self._size
