""" This module contains the class Linked List for a Data Structure representation """
from typing import Any
from node import Node

class LinkedList:
    """This class creates a Linked List from multiple Nodes objects 
     (Single Linked List) """

    def __init__(self) -> None:
        """
         Initialize a Linked List structure. This defines  the Double Linked List 
         operations for the nodes
        """
        #initializing the first and last elements of the list
        self.head : Node = None
        self.tail : Node = None
        self.lenght : int = 0

    def append (self, data: Any) -> None:
        """Adds a element to the the tail of the list"""
        new_node : Node = Node(data)

        if self.tail is  None:
            # the only element on the list
            self.head = self.tail = new_node
        else:
            #updating next
            self.tail.next = new_node
            #adding a new tail
            self.tail = new_node
        self.lenght += 1

    def prepend(self, data: Any) -> None:
        """Adds a element to the the head of the list """
        new_node : Node = Node(data)

        if self.head is  None:
            # the only element on the list
            self.head = self.tail = new_node
        else:
            # Point the new node's next to the current head
            new_node.next = self.head
            # Update the head to the new node
            self.head = new_node
        self.lenght += 1

    def lookup(self, data: Any) -> int:
        """Finds the index of the element by value (the first one found)."""
        current = self.head
        index = 0

        # Traverse the list
        while current is not None:
            if current.data == data:  # Compare the data
                return index
            current = current.next  # Move to the next node
            index += 1  # Increment the index

        # If we reach here, the data was not found
        raise ValueError("Item is not in the list")

    def insert(self, index: int, data: Any) -> None:
        """
        Insert the element at a specific index with the elements shifted to the right
        
        If index is 0 uses prepennd, if index is length uses appends
        """

        if index == 0:
        # Insert at the beginning
            self.prepend(data)
            return

        if index == self.lenght:
            # Insert at the end
            self.append(data)
            return

        # Insert in the middle
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):  # Stop at the node before the desired index
            current = current.next

        if current.next == self.tail:
            self.tail = current

        # Update links to insert the new node
        new_node.next = current.next
        current.next = new_node

        self.lenght += 1

    def delete(self, index : int) -> None:
        """Deletes the element by index."""
        current = self.head

        if index == 0:
            # delete at the beginning
            current = self.head.next
            self.head = current
            self.lenght -= 1
            return

        # delete at the middle
        for _ in range(index-1):  # Stop at the node before the desired index
            current = current.next

        if current.next == self.tail:
            #deleting at the end
            self.tail = current

        current.next = current.next.next
        self.lenght -= 1

    def __str__(self) -> str:
        """Returns the string representation for the Linked List class instances"""
        nodes = []
        current = self.head
        # Traverse the list
        while current is not None:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes)
