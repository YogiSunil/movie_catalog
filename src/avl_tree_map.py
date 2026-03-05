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
        self._root, inserted = self._insert(self._root, key, value)
        if inserted:
            self._size += 1

    def get(self, key: K) -> Optional[V]:
        current = self._root
        while current is not None:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current.value
        return None

    def delete(self, key: K) -> bool:
        self._root, deleted = self._delete(self._root, key)
        if deleted:
            self._size -= 1
        return deleted

    def items(self) -> Generator[tuple[K, V], None, None]:
        yield from self._items(self._root)

    def range(self, low: K, high: K) -> Generator[tuple[K, V], None, None]:
        if low > high:
            return
        yield from self._range(self._root, low, high)

    def height(self) -> int:
        return self._height(self._root)

    def __len__(self) -> int:
        return self._size

    @staticmethod
    def _height(node: Optional[_Node[K, V]]) -> int:
        return node.height if node is not None else 0

    def _update_height(self, node: _Node[K, V]) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: _Node[K, V]) -> int:
        return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, node: _Node[K, V]) -> _Node[K, V]:
        new_root = node.right
        if new_root is None:
            return node

        node.right = new_root.left
        new_root.left = node

        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node: _Node[K, V]) -> _Node[K, V]:
        new_root = node.left
        if new_root is None:
            return node

        node.left = new_root.right
        new_root.right = node

        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rebalance(self, node: _Node[K, V]) -> _Node[K, V]:
        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1:
            if node.left is not None and self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1:
            if node.right is not None and self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _insert(self, node: Optional[_Node[K, V]], key: K, value: V) -> tuple[_Node[K, V], bool]:
        if node is None:
            return _Node(key=key, value=value), True

        if key < node.key:
            node.left, inserted = self._insert(node.left, key, value)
        elif key > node.key:
            node.right, inserted = self._insert(node.right, key, value)
        else:
            node.value = value
            return node, False

        return self._rebalance(node), inserted

    def _delete(self, node: Optional[_Node[K, V]], key: K) -> tuple[Optional[_Node[K, V]], bool]:
        if node is None:
            return None, False

        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            successor = self._min_node(node.right)
            node.key = successor.key
            node.value = successor.value
            node.right, _ = self._delete(node.right, successor.key)
            deleted = True

        if not deleted:
            return node, False

        return self._rebalance(node), True

    def _min_node(self, node: _Node[K, V]) -> _Node[K, V]:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _items(self, node: Optional[_Node[K, V]]) -> Generator[tuple[K, V], None, None]:
        if node is None:
            return
        yield from self._items(node.left)
        yield (node.key, node.value)
        yield from self._items(node.right)

    def _range(self, node: Optional[_Node[K, V]], low: K, high: K) -> Generator[tuple[K, V], None, None]:
        if node is None:
            return

        if low < node.key:
            yield from self._range(node.left, low, high)
        if low <= node.key <= high:
            yield (node.key, node.value)
        if node.key < high:
            yield from self._range(node.right, low, high)
