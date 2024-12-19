""" This module contains the class stack for a Data Structure representation """
from typing import Any
from node import Node

class Stack:
    """This class creates a stack from multiple Nodes objects 
     (Singly Linked List) """

    def __init__(self) -> None:
        """
        Initialize a Stack instance. This defines  the LIFO operations
        for the nodes
        """
        #initializing the element on the top of the stack
        self.top: Node = None

    def push(self, data: Node) -> None:
        """Add a node to the top of the structure"""
        new_node : Node = Node(data)
        #next is the previous element on top
        new_node.next = self.top
        #this new node will be on the  top
        self.top = new_node

    def pop(self) -> None:
        """Delete the element on top of the stack"""
        if self.top is  None:
            print ('The stack is empty')
        # set the next element as the top of the stack
        self.top = self.top.next

    def peak(self) -> Any:
        """Returns the element on top of the stack"""
        if self.top is  None:
            return 'The stack is empty'
        return self.top.data

    def is_empty(self) -> bool:
        """Returns True if the stack is empty"""
        return self.top is None
