"""Test functions for bs_tree module."""
import pytest
from bs_tree import BinarySeachTree

@pytest.fixture
def bst():
    """Fixture to create an empty tree for each test"""
    return BinarySeachTree()

@pytest.mark.parametrize("values, lookup_value, expected_found", [
    ([10, 5, 15], 10, True),
    ([10, 5, 15], 5, True),
    ([10, 5, 15], 15, True),
    ([10, 5, 15], 100, False),
])
def test_insert_and_lookup(bst, values, lookup_value, expected_found):
    """Testing the insert and lookup functions for BinarySeachTree class"""
    for value in values:
        bst.insert(value)
    result = bst.lookup(lookup_value)
    if expected_found:
        assert result is not None
    else:
        assert result is None

@pytest.mark.parametrize("values, delete_value, remaining_values", [
    ([10, 5, 15], 5, [10, 15]),
    ([10, 5, 15], 15, [10, 5]),
])
def test_delete_leaf_node(bst, values, delete_value, remaining_values):
    """Testing the delete functions for BinarySeachTree class: leaf case"""
    for value in values:
        bst.insert(value)
    bst.delete(delete_value)
    assert bst.lookup(delete_value) is None
    for val in remaining_values:
        assert bst.lookup(val) is not None

@pytest.mark.parametrize("values, delete_value, remaining_values", [
    ([10, 5, 15, 7], 5, [10, 7, 15]),
    ([10, 5, 15, 12], 15, [10, 5, 12]),
])
def test_delete_node_with_one_child(bst, values, delete_value, remaining_values):
    """Testing the delete functions for BinarySeachTree class: one child case"""
    for value in values:
        bst.insert(value)
    bst.delete(delete_value)
    assert bst.lookup(delete_value) is None
    for val in remaining_values:
        assert bst.lookup(val) is not None

@pytest.mark.parametrize("values, delete_value, remaining_values", [
    ([10, 5, 15, 3, 7, 12, 18], 5, [10, 3, 7, 15, 12, 18]),
])
def test_delete_node_with_two_children(bst, values, delete_value, remaining_values):
    """Testing the delete functions for BinarySeachTree class: two children case"""
    for value in values:
        bst.insert(value)
    bst.delete(delete_value)
    assert bst.lookup(delete_value) is None
    for val in remaining_values:
        assert bst.lookup(val) is not None

@pytest.mark.parametrize("lookup_value, expected_result", [
    (10, None),  # Testing an empty tree
])
def test_empty_tree(bst, lookup_value, expected_result):
    """Testing the lookup function for BinarySeachTree class: leaf case"""
    result = bst.lookup(lookup_value)
    assert result == expected_result
