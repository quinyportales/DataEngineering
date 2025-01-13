"""Test functions for linked_list, stack and queue_struc modules."""
import pytest
from linked_list import LinkedList
from stack import Stack
from queue_struc import QueueStruct

@pytest.fixture
def linked_list():
    """Fixture to create an empty linked list for each test"""
    return LinkedList()

def get_linked_list_test_data_append():
    """Reusable test data for linked list append method: input_values, 
    expected_length, expected_head, expected_tail"""
    return [
        ([10], 1, 10, 10),
        ([10, 20], 2, 10, 20),
        ([10, 20, 30], 3, 10, 30),
        ([5, 10, 15, 20], 4, 5, 20),
    ]

@pytest.mark.parametrize("input_values, expected_length, expected_head, expected_tail",
                        get_linked_list_test_data_append())
def test_append(linked_list, input_values, expected_length, expected_head, expected_tail):
    """Testing the append function for LinkedList class adding multiple nodes 
    and checking the tail, head and length"""
    for value in input_values:
        linked_list.append(value)
    assert linked_list.lenght == expected_length
    assert linked_list.head.data == expected_head
    assert linked_list.tail.data == expected_tail

@pytest.mark.parametrize(
    "input_values, expected_length, expected_head, expected_tail",
    [
        ([10], 1, 10, 10),
        ([10, 20], 2, 20, 10),
        ([10, 20, 30], 3, 30, 10),
        ([5, 10, 15, 20], 4, 20, 5),
    ]
)

def test_prepend(linked_list, input_values, expected_length, expected_head, expected_tail):
    """Testing the preprend function for LinkedList class adding multiple nodes 
    and checking the tail, head and lenght"""
    for value in input_values:
        linked_list.prepend(value)
    assert linked_list.lenght == expected_length
    assert linked_list.head.data == expected_head
    assert linked_list.tail.data == expected_tail


@pytest.mark.parametrize(
    "input_values, lookup_value, expected_index",
    [
        ([10], 10, 0),
        ([10, 20], 10, 0),
        ([10, 20], 20, 1),
        ([10, 20, 30], 20, 1),
        ([5, 10, 15, 20], 15, 2),
    ]
)

def test_lookup(linked_list, input_values, lookup_value, expected_index):
    """Testing the lookup function for LinkedList class"""
    for value in input_values:
        linked_list.append(value)
    assert linked_list.lookup(lookup_value) == expected_index

@pytest.mark.parametrize(
    "input_values, index, data_value, expected_output",
    [
        ([10], 0, 9, [9,10]),
        ([10, 20], 1, 15, [10,15,20]),
        ([10, 20], 0, 15, [15,10,20]),
        ([10, 20, 30], 1, 15, [10,15,20,30]),
    ]
)

def test_insert(linked_list, input_values, index, data_value, expected_output):
    """Testing the insert function for LinkedList class"""
    for value in input_values:
        linked_list.append(value)
    linked_list.insert(index, data_value)
    result = list(linked_list)
    assert result == expected_output

@pytest.mark.parametrize(
    "input_values, index, expected_output",
    [
        ([10], 0, []),
        ([10, 20], 1, [10]),
        ([10, 20], 0, [20]),
        ([10, 15, 20, 30], 1, [10,20,30]),
    ]
)
def test_delete(linked_list, input_values, index, expected_output):
    """Testing the delete function for LinkedList class"""
    for value in input_values:
        linked_list.append(value)
    linked_list.delete(index)
    result = list(linked_list)
    assert result == expected_output

@pytest.fixture
def stack():
    """Fixture to create an empty stack  for each test"""
    return Stack()

@pytest.mark.parametrize("input_values, expected_length, expected_head, expected_tail",
                         get_linked_list_test_data_append())
def test_push(stack, input_values, expected_length, expected_head, expected_tail):
    """Test the push method for Stack class which extends from the Class LinkedList"""
    for value in input_values:
        stack.push(value)
    assert stack.lenght == expected_length
    assert stack.head.data == expected_head
    assert stack.tail.data == expected_tail

@pytest.mark.parametrize(
    "input_values, expected_output", 
    [
        ([10], []),
        ([10, 20], [10]),
        ([10, 20, 30], [10, 20]),
        ([5, 10, 15, 20], [5, 10, 15]),
    ]
)
def test_pop(stack, input_values, expected_output):
    """Test the pop function for Stack class"""
    for value in input_values:
        stack.append(value)
    stack.pop()
    result = list(stack)
    assert result == expected_output

@pytest.mark.parametrize(
    "input_values, expected_output", 
    [
        ([10], 10),
        ([10, 20], 20),
        ([10, 20, 30], 30),
        ([5, 10, 15, 20], 20),
        ([], "The stack is empty")
    ]
)
def test_peak_stack(stack, input_values, expected_output):
    """Test the peak function for Stack class"""
    for value in input_values:
        stack.append(value)
    result = stack.peak()
    assert result == expected_output

@pytest.mark.parametrize(
    "input_values, expected_output", 
    [
        ([], True),
        ([10], False),
        ([10, 20], False),
        ([5, 10, 15, 20], False)
    ]
)
def test_is_empty(stack, input_values, expected_output):
    """Test the is_empty function for Stack class"""
    for value in input_values:
        stack.append(value)
    result = stack.is_empty()
    assert result == expected_output

@pytest.fixture
def queue():
    """Fixture to create an empty queue for each test"""
    return QueueStruct()

@pytest.mark.parametrize("input_values, expected_length, expected_head, expected_tail",
                         get_linked_list_test_data_append())
def test_enqueue(queue, input_values, expected_length, expected_head, expected_tail):
    """Test the enqueue method for QueueStruct class which extends from the Class LinkedList"""
    for value in input_values:
        queue.enqueue(value)
    assert queue.lenght == expected_length
    assert queue.head.data == expected_head
    assert queue.tail.data == expected_tail


@pytest.mark.parametrize(
    "input_values, expected_output", 
    [
        ([10], 10),
        ([10, 20], 10),
        ([10, 20, 30], 10),
        ([5, 10, 15, 20], 5),
        ([], "The queue is empty")
    ]
)
def test_peak_queue(queue, input_values, expected_output):
    """Test the peak function for QueueStruct class"""
    for value in input_values:
        queue.append(value)
    result = queue.peak()
    assert result == expected_output

@pytest.mark.parametrize(
    "input_values, expected_output", 
    [
        ([10], []),
        ([10, 20], [20]),
        ([10, 20, 30], [20, 30]),
        ([5, 10, 15, 20], [10, 15, 20]),
    ]
)
def test_dequeue(queue, input_values, expected_output):
    """Test the pop function for QueueStruct class"""
    for value in input_values:
        queue.append(value)
    queue.dequeue()
    result = list(queue)
    assert result == expected_output
