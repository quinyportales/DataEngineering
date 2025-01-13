""" This module contains the Binary Search, Bubble Sort 
and Recursive Factorial Functions  """
from typing import Any

def binary_search(arr, target) -> int:
    """
    Perform a binary search on a sorted list to find the target element.

    The function sorts the input list using Bubble Sort before performing the search.

    Parameters:
    arr (List[Any]): The list of elements to search through.
    target (Any): The element to find in the list.

    Returns:
    int: The index of the target element if found, otherwise -1.
    """
    #sorting the arr
    bubble_sort(arr)
    #left is the first element and right the last element of my list
    left = 0
    right =  len(arr) - 1
    while left <= right:
        #middle index for the list
        mid = (left + right) // 2
        #checking if the middle value is the target value
        if arr[mid] == target:
            return mid

        #if the middle value is less than the target we search on the left side
        if arr[mid] < target:
            left = mid + 1
        #if the middle value is greater than the target we search on the right side
        else:
            right = mid - 1
    return -1  # Not found

def bubble_sort(arr)-> list[Any]:
    """
    Sort a list using the Bubble Sort algorithm.

    Parameters:
    arr (List[Any]): The list of elements to be sorted.

    Returns:
    List[Any]: The sorted list.
    """
    n = len(arr)
    for i in range(n):
        #initializes in each iteration to check if there were changes on the list
        swapped = False
        for j in range(0, n - i - 1):
            #comparing the adjacents elements and taking the greater to the end
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            #we break the loop is nothing has been swapped
            break
    return arr

def recursive_factorial(n) -> int:
    """
    Compute the factorial of a non-negative integer using recursion.

    Parameters:
    n (int): The non-negative integer to compute the factorial for.

    Returns:
    int: The factorial of the given integer.
    """
    #base case
    if n in (0, 1):
        return 1
    return n * recursive_factorial(n - 1)
