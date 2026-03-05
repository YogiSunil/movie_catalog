from src.avl_tree_map import AVLTreeMap


def _inorder_keys(tree: AVLTreeMap[str, int]) -> list[str]:
    return [key for key, _ in tree.items()]


def _build_tree(keys: list[str]) -> AVLTreeMap[str, int]:
    tree: AVLTreeMap[str, int] = AVLTreeMap()
    for index, key in enumerate(keys):
        tree.set(key, index)
    return tree


def test_ll_rotation() -> None:
    tree = _build_tree(["c", "b", "a"])
    assert _inorder_keys(tree) == ["a", "b", "c"]
    assert tree._root is not None
    assert tree._root.key == "b"


def test_rr_rotation() -> None:
    tree = _build_tree(["a", "b", "c"])
    assert _inorder_keys(tree) == ["a", "b", "c"]
    assert tree._root is not None
    assert tree._root.key == "b"


def test_lr_rotation() -> None:
    tree = _build_tree(["c", "a", "b"])
    assert _inorder_keys(tree) == ["a", "b", "c"]
    assert tree._root is not None
    assert tree._root.key == "b"


def test_rl_rotation() -> None:
    tree = _build_tree(["a", "c", "b"])
    assert _inorder_keys(tree) == ["a", "b", "c"]
    assert tree._root is not None
    assert tree._root.key == "b"
