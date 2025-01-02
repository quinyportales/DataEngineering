"""Module Contains Stock class"""
from .item import OrderedItem


class Stock:
    """Class representing the available stock from a restaurant
    It contains the quantities for each item on the menu"""

    def __init__(self) -> None:
        """
        Initialize a Stock instance.
        """
        self.inventory: dict[str:int]={}

    def add_stock(self,item_name: str, quantity: int) -> None:
        """Add an item or increment its quantity
        Parameters:
        item_name: str - Name of one item from the menu.
        quantity: int - Quantity available for this item.
        """

        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name]=quantity

    def deduct_item(self, item: OrderedItem) -> None:
        """
        Deduct the stock quantity from a ordered item

        Parameters:
        item (OrderedItem): An instance from the OrderedItem class representing the item ordered.
        """

        if item.item_name in self.inventory:
            # if available
            if self.inventory[item.item_name] >= item.quantity:
                self.inventory[item.item_name] -= item.quantity
                print(f"{item.quantity} units of {item.item_name} deducted from stock.")

                # Delete the item from stock if item quantity is cero
                if self.inventory[item.item_name] == 0:
                    del self.inventory[item.item_name]
            else:
                print(f"Not enough {item.item_name} in stock."
                f"Available: {self.inventory[item.item_name]}")
        else:
            print(f"{item.item_name} not in stock.")
