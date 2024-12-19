"""This module implements the classes Data Structure representation"""
from linked_list import LinkedList
from queue_struc import QueueStruct
from stack import Stack
from bs_tree import BinarySeachTree

if __name__ == '__main__':
    #Implementing the Linked List structure
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    # Displaying the head of the list (should be 1)
    print("***Working Linked Lists***")
    print(linked_list.head.data)

    # Displaying the head of the list (should be 3)
    print(linked_list.tail.data)

    #prepending elements
    linked_list.prepend("new head")

    #appending elements
    linked_list.append("new tail")

    # Displaying the head of the list (should be 'new head')
    print(linked_list.head.data)

    # Displaying the head of the list (should be 'new tail')
    print(linked_list.tail.data)

    # Displaying the lenght of the list (should be 5)
    print(linked_list.lenght)

    # Insert at the beginning
    linked_list.insert(0, "updated head")
    print("After inserting at index 0:")
    print(linked_list)


    # Insert in the middle
    linked_list.insert(2, "middle element")
    print("After inserting at index 2:")
    print(linked_list)

    # Insert at the end
    linked_list.insert(linked_list.lenght, "updated tail")
    print("After inserting at the end:")
    print(linked_list)

    # Display the length of the list
    print("New length of the list:", linked_list.lenght)

    # Delete at the beginning
    print("After deleting at the beginning:")
    linked_list.delete(0)
    print(linked_list)

    # Display the length of the list (should be 7)
    print("New length of the list:", linked_list.lenght)

    # Delete at the middle
    print("After deleting at the middle:")
    linked_list.delete(3) #removing the data 2
    # Displaying the list (number 2 must be removed)
    print(linked_list)

    # Display the length of the list (should be 6)
    print("New length of the list:", linked_list.lenght)

    # Delete at the end
    print("After deleting at the end:")
    linked_list.delete(linked_list.lenght - 1) #removing the tail
    # Displaying the list
    print(linked_list)

    # Display the length of the list (should be 5)
    print("New length of the list:", linked_list.lenght)

    #Implementing the queue structure
    print("\n ***Working Queues***")
    queue = QueueStruct()
    # Displaying the head of the queue
    print("The head of the queue:", queue.peak())

    queue.enqueue("first")
    queue.enqueue("second")
    queue.enqueue("third")

    # Displaying the hea  of the queue (should be first)
    print("The head of the queue:", queue.peak())

    #deleting the head of the queue
    queue.dequeue()
    # Displaying the hea  of the queue (should be second)
    print("The head of the queue:", queue.peak())

    #deleting the head of the queue
    queue.dequeue()
    # Displaying the hea  of the queue (should be third)
    print("The head of the queue:", queue.peak())

    #Implementing the stack structure
    # Instantiating a Stack object
    stack = Stack()

    # Checking if the stack is empty
    print("\n ***Working Stacks***")
    print("is empty?",stack.is_empty())
    # Pushing items onto the stack
    stack.push(1)
    stack.push(2)
    stack.push(3)

    # Displaying the top of the stack (should be 3)
    print("Top of the stack:", stack.peak())

    # Popping the top item and showing the new top
    stack.pop()
    print("Top after one pop:", stack.peak())
    # Checking if the stack is empty
    print("is empty?",stack.is_empty())

    # Popping another item and showing the new top
    stack.pop()
    print("Top after another pop:", stack.peak())  # Expected output: 1

    # Popping the last item
    stack.pop()
    print("is empty?", stack.is_empty())


    #Implementing the Binary Tree structure
    print("\n ***Working Binary Trees***")
    bs_tree = BinarySeachTree()
    #inserting values
    bs_tree.insert(20)
    bs_tree.insert(10)
    bs_tree.insert(7)
    bs_tree.insert(18)
    bs_tree.insert(2)
    bs_tree.insert(9)
    bs_tree.insert(15)

    bs_tree.insert(25)
    bs_tree.insert(24)
    bs_tree.insert(21)
    bs_tree.insert(32)
    bs_tree.insert(28)
    bs_tree.insert(41)
    bs_tree.insert(37)

    #searching for an existing value on the binary tree
    found_node = bs_tree.lookup(28)
    if found_node:
        print(f"Node found with value: {found_node.data}")
    else:
        print("Value not found in the tree.")

    #searching for a non existing value on the binary tree
    found_node = bs_tree.lookup(600)
    if found_node:
        print(f"Node found with value: {found_node.data}")
    else:
        print("Value not found in the tree.")

    #deleting a leaf
    bs_tree.delete(28)

    #deleting a node with one child
    bs_tree.delete(18)

    #deleting a node with two children
    bs_tree.delete(25)
    