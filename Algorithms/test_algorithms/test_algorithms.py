"""Test functions for algorithm module."""
import pytest
from ..algorithms import binary_search, bubble_sort, recursive_factorial

@pytest.mark.parametrize('input_values, expected',
                         [
                             ([22, 96, 2, 1, 2, 67, 68, 25, 17, 5, 31],
                              [1, 2, 2, 5, 17, 22, 25, 31, 67, 68, 96]),
                              ([100_000, 123, 129_450, -193, 972, -59, 3],
                              [-193, -59, 3, 123, 972, 100_000, 129_450]),
                              ([-23, 98, 0, -3, -5, 145, 2.5],
                               [-23, -5, -3, 0, 2.5, 98, 145])
                         ])

def test_bubble_sort(input_values, expected):
    """Testing bubble_sort."""
    arr = input_values
    assert bubble_sort(arr) == expected


@pytest.mark.parametrize('input_values, expected',
                         [
                             (([22, 96, 2, 1, 2, 67, 68, 25, 17, 5, 31], 25), 6),
                             (([22, 96, 2, 1, 2, 67, 68, 25, 17, 5, 31], 96), 10),
                             (([22, 96, 2, 1, 2, 67, 68, 25, 17, 5, 31], 100), -1)
                         ])

def test_binary_search(input_values, expected):
    """Testing binary_search function."""
    arr, target = input_values
    assert binary_search(arr, target) == expected


@pytest.mark.parametrize('input_values, expected', [
    (0,1),
    (5,120),
    (7,5040)
    ])

def test_recursive_factorial(input_values, expected):
    """Testing recursive_factorial."""
    assert recursive_factorial(input_values) == expected
