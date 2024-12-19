""" This module contains the classes Node and Binary Tree non linear 
Data Structure representation """
from typing import Any

class Node:
    """This class creates a data node and set the pointer to the next 
    node in a hierarchical structure """

    def __init__(self, data: Any) -> None:
        """
        Initialize a Node instance. The pointer to the next node is 
        initialized as none 

        Parameters:
        data: Any - any type of data to be stored in this node
        """
        self.data : Any = data
        self.left: Node = None
        self.right : Node = None

class BinarySeachTree:
    """This class creates a Binary Search Tree structure from multiple Nodes objects """
    def __init__(self) -> None:
        """
         Initialize a Node instance. The root node is 
         initialized as none 
         """
        self.root : Node = None

    def insert(self, data : Any) -> None:
        """Adds an element to the tree structure"""
        new_node : Node = Node (data)

        #Checking if the tree is empty
        if not self.root:
            self.root = new_node
            return
        current = self.root
        while data != current.data:
            #evaluating the left side
            if data < current.data:
                # checking if there is an existent left value
                if not current.left:
                    current.left = new_node
                    break
                #if we already have a left node then we update the current node
                current = current.left
            else:
                # checking if there is an existent right  value
                if not current.right:
                    current.right = new_node
                    break
                #if we already have a right node then we update the current node
                current = current.right
        return

    def lookup(self, data: Any) -> Node:
        """
        Finds a node in the binary search tree by its value and returns the node.
    
        Parameters:
        data: Any - the value to search for in the tree.
    
        Returns:
        Node - the node containing the value, or None if the value is not found.
        """
        current = self.root
        while current:
            if data == current.data:
                return current  # Found the value
            if data < current.data:
                current = current.left  # Go to the left subtree
            else:
                current = current.right  # Go to the right subtree
        return None  # Value not found

    def delete(self, data: Any, start: Node = None, parent: Node = None) -> None:
        """
        Deletes a node with the specified value from the tree.

        Parameters:
        - data (Any): The value to be deleted.
        - start (Optional[Node]): The starting point for the search (default: root).
        - parent (Optional[Node]): The parent node of the current node.

        Raises:
        - Exception: If the value is not found in the tree.
        """
        current = start or self.root
        while current and current.data != data:
            parent = current
            if data < current.data:
                current = parent.left
            else:
                current = parent.right
        if not current:
            #if the node is not in tree
            raise ValueError("Item not in tree")

        #checking the childrens
        if not current.left and not current.right:
            #if the node has no childrens
            return self._remove_node_no_children(current, parent)
        if current.left and current.right:
            #if the node has two childrens
            print (f"Two children node {current.data} successfully deleted")
            return self._remove_node_two_children(current)
        #if the node has one child
        return self._remove_node_one_child(current, parent)

    def _remove_node_no_children(self, current: Node, parent: Node) -> None:
        """
        Removes a node with no children (leaf node).

        Parameters:
        - current (Node): The node to be removed.
        - parent (Optional[Node]): The parent node of the current node.
        """
        if current is self.root:
            #removing the root if this is the only node in tree
            self.root = None
            return self
        if parent.left == current:
            parent.left = None
        else:
            parent.right = None
        print(f"Leaf node {current.data} successfully deleted")
        return self

    def _remove_node_one_child(self, current: Node, parent: Node) -> None:
        """
        Removes a node with one child.

        Parameters:
        - current (Node): The node to be removed.
        - parent (Optional[Node]): The parent node of the current node.
        """
        #checking if the value is the root and setting the child as the new root
        if current is self.root:
            self.root = current.right if current.right else current.left
            return self

        #if the current node is not the root
        if parent.right == current:
            #is current located to the right of the parent?
            parent.right = current.right if current.right else current.left
        else:
            parent.left = current.right if current.right else current.left
        print(f"One child node {current.data} successfully deleted")
        return self

    def _remove_node_two_children(self, current: Node) -> None:
        """
        Removes a node with two children by replacing it with its successor.

        Parameters:
        - current (Node): The node to be removed.
        """
        #finding the succesor which will replace the deleted node
        successor = self._get_successor(current)
        current.data = successor.data # Replace current node's value with successor's value
        # Remove the successor node
        return self.delete(successor.data, current.right, current )

    @staticmethod
    def _get_successor(current: Node) -> Node:
        """
        Finds the successor of a node (smallest node in the right subtree).

        Parameters:
        - current (Node): The node whose successor is to be found.

        Returns:
        - Node: The successor node.
        """
        #we go to right one time
        successor = current.right
        while successor and successor.left:
            #we then go to left until we find the successor
            successor = successor.left
        return successor
