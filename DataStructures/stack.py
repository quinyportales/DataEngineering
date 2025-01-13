""" This module contains the class stack for a Data Structure representation """
from typing import Any
from linked_list import LinkedList
from node import Node

class Stack (LinkedList):
    """This class creates a stack from multiple Nodes objects 
     (Singly Linked List) """

    def __init__(self) -> None:
        """
        Initialize a Stack instance. This defines  the LIFO operations
        for the nodes
        """
        #initializing the element on the top of the stack
        super().__init__()

    def push(self, data: Node) -> None:
        """Add a node to the top of the structure"""
        self.append(data)

    def pop(self) -> None:
        """Delete the element on top of the stack"""
        if self.tail is  None:
            print ('The stack is empty')
        # set the next element as the top of the stack
        super().delete(self.lenght -1)

    def peak(self) -> Any:
        """Returns the element on top of the stack"""
        if self.tail is  None:
            return 'The stack is empty'
        return self.tail.data

    def is_empty(self) -> bool:
        """Returns True if the stack is empty"""
        return self.tail is None
