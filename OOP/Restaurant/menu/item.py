"""Module Contains classes Item, OrderedItem"""
from employee_and_customer.customer import Customer
from employee_and_customer.employee import Employee
from menu.menu_class import Menu


class Item:
    """
    Models items for a menu in a Restaurant with name, price, and category.
    """

    def __init__(self, category: str ,item_name: str , price: float) -> None:
        """
        Initialize an Item instance.

        Parameters:
        category: str - Food category.
        item_name: str - Name of the item.
        price: float - Price of the item.
        """
        self.item_name: str = item_name
        self.price: float = price
        self.category: str = category

    def add_item(self) -> dict:
        """
        Add elements to the Menu.

        Parameters:
        menu: Menu - Instance of Menu class.
        """
        item_dic = {self.category:{self.item_name:self.price}}
        return(item_dic)


class OrderedItem(Item):
    """
    Models an item ordered by a customer from the menu.
    """

    def __init__(self,date: str ,item: Item, quantity: int, customer: Customer) -> None:
        """
        Initialize an OrderedItem instance.

        Parameters:
        date: str - Date when the order is placed.
        item: Item - Instace from the parent class.
        quantity: int.
        customer: Instance from the Customer class 
        """
        super().__init__(item.category, item.item_name , item.price)
        self.date: str =date
        self.quantity: int = quantity
        self.customer: Customer = customer

    def calculate_total(self) -> float:
        """Returns the product from the quantity and price for the ordered item"""
        return self.price * self.quantity

    def show_details(self) -> None:
        """Show the details for the ordered item"""
        print("Ordered Item")
        print(f'Date: {self.date}\n'
              f'Ordered Item: {self.item_name}\n'
              f'Item Price: {self.price} \n'
              f'Quantity: {self.quantity} \n'
              f'Total Amount: {self.calculate_total()} \n')

    def __str__(self) -> str:
        """Returns the string representation for an OrderedItem instance."""
        return f"Item: {self.item_name}, Category: {self.category} "

    def __repr__(self)->str:
        """Returns the string representation of the OrderedItem instance."""
        return self.__str__()

