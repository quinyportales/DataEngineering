""" This module contains the class Node for  Linear Data Structures representation """
from typing import Any

class Node:
    """This class creates a data node and set the pointer to the next node 
     (Singly Linked List) """

    def __init__(self, data) -> None:
        """
         Initialize a Node instance. The pointer to the next node is 
         initialized as none 

         Parameters:
         data: Any - any type of data to be stored in this node
         """
        self.data: Any = data
        self.next : Node = None
