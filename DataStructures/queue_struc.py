""" This module contains the class queue for a Data Structure representation """
from typing import Any
from linked_list import LinkedList

class QueueStruct (LinkedList):
    """This class creates a queue from multiple Nodes objects 
     (Single Linked List) """

    def __init__(self) -> None:
        """
        Initialize a Queue_Struct instance. This defines  the FIFO operations
        for the nodes
        """
        super().__init__()

    def enqueue(self, data) -> None:
        """Adding a node to the end of queue"""
        #creating a node
        self.append(data)

    def peak(self) -> Any:
        """Returns the head element of the queue"""
        if self.head is  None:
            return"The queue is empty"
        return self.head.data

    def dequeue(self) -> None:
        """This deletes the node on the head of the queue"""
        if self.head is  None:
            print("The queue is empty")
        super().delete(0)
