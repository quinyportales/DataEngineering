""" This module contains the class queue for a Data Structure representation """
from typing import Any
from node import Node

class QueueStruct:
    """This class creates a queue from multiple Nodes objects 
     (Singly Linked List) """

    def __init__(self) -> None:
        """
        Initialize a Queue_Struct instance. This defines  the FIFO operations
        for the nodes
        """
         #initializing the first and last elements of the queue
        self.head: Node = None
        self.tail: Node = None

    def enqueue(self, data) -> None:
        """Adding a node to the end of queue"""
        #creating a node
        new_node : Node = Node(data)

        if self.tail is  None:
            # the only element on the queue
            self.head = self.tail = new_node
        else:
            #updating next
            self.tail.next = new_node
            #adding a new tail
            self.tail = new_node

    def peak(self) -> Any:
        """Returns the head element of the queue"""
        if self.head is  None:
            return"The queue is empty"
        return self.head.data

    def dequeue(self) -> None:
        """This deletes the node on the head of the queue"""
        if self.head is  None:
            print("The queue is empty")
        self.head = self.head.next
