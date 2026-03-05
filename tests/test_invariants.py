from __future__ import annotations

import random

from src.avl_tree_map import AVLTreeMap, _Node


def _assert_invariants(node: _Node[str, int] | None) -> int:
    if node is None:
        return 0

    left_height = _assert_invariants(node.left)
    right_height = _assert_invariants(node.right)

    if node.left is not None:
        assert node.left.key < node.key
    if node.right is not None:
        assert node.right.key > node.key

    balance = left_height - right_height
    assert -1 <= balance <= 1

    expected_height = 1 + max(left_height, right_height)
    assert node.height == expected_height
    return expected_height


def test_randomized_invariants_insert_delete() -> None:
    tree: AVLTreeMap[str, int] = AVLTreeMap()
    rng = random.Random(42)

    keys = [f"movie-{n:04d}" for n in range(1000)]
    rng.shuffle(keys)

    active: set[str] = set()
    for index, key in enumerate(keys):
        tree.set(key, index)
        active.add(key)
        _assert_invariants(tree._root)

    assert len(tree) == 1000

    to_delete = rng.sample(keys, 200)
    for key in to_delete:
        assert tree.delete(key) is True
        active.remove(key)
        _assert_invariants(tree._root)

    assert len(tree) == 800
    for key in active:
        assert tree.get(key) is not None
    for key in to_delete:
        assert tree.get(key) is None


def test_update_existing_key_does_not_change_size() -> None:
    tree: AVLTreeMap[str, int] = AVLTreeMap()
    tree.set("the matrix", 1)
    tree.set("the matrix", 2)
    assert len(tree) == 1
    assert tree.get("the matrix") == 2
