"""Module Contains Order class"""
from employee_and_customer.customer import Customer
from menu.item import OrderedItem


class Order:
    """Class representing the order for a lis of items from the menu."""
    #initializing the uniques id's

    _id_counter = 1

    def __init__(self, customer: Customer) -> None:
        self._order_id: int = Order._id_counter
        Order._id_counter+=1
        self.customer: Customer = customer
        self.ordered_items: list[OrderedItem]= []
        self.status: str = "Pending"  #initial order status
        self.total: float = 0

    @property
    def order_id(self) -> int:
        """order id getter"""
        return self._order_id

    def add_item(self, ordered_item: OrderedItem)-> None:
        """adds and ordered item to the order
        Parameters:
        OrderedItem: An instance from the OrderedItem class representing the item ordered.
        """
        self.ordered_items.append(ordered_item)
        self.total += ordered_item.calculate_total()

    def calculate_total(self) -> float:
        """Return the total amount of the order"""
        return sum(item.calculate_total() for item in self.ordered_items)

    def show_details(self) -> None :
        """Prints out the details for the order"""
        self.total= self.calculate_total()
        print("Order Receipt")
        print(f'Order ID: {self.order_id}\n'
              f'Customer : {self.customer.name}\n'
              f'Ordered Item: {self.ordered_items}\n'
              f'Total Amount: {self.total} \n')

    def complete_order(self) -> None:
        """Update the order status"""
        self.status='Completed'
