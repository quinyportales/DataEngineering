"""Module Contains classes Item, OrderedITem, Stock, Order, Payment  and Delivery from a 
restaurant classes representation"""

from restaurant import Customer
from employee import Employee

class Item:
    """Class representing the single item from menu"""
    def __init__(self, category,item_name, price) -> None:
        self.item_name = item_name
        self.price=price
        self.category=category
        self.item_dic = None

    def add_item(self, menu):
        """Adds an item to menu"""
        self.item_dic ={self.category:{self.item_name:self.price}}
        menu.add_menu(self.item_dic)

class OrderedItem(Item):
    """Class representing an Item ordered by a customer"""

    def __init__(self,date: str ,item: Item, quantity: int, customer: Customer) -> None:
        super().__init__(item.category, item.item_name, item.price)
        self.date=date
        self.quantity = quantity
        self.customer= customer
        self.total=None

    def calculate_total(self):
        """Returns the product from the quantity and price for the ordered item"""
        return self.price * self.quantity

    def show_details(self):
        """Show the details for the ordered item"""
        self.total= self.calculate_total()
        print("Ordered Item")
        print(f'Date: {self.date}\n'
              f'Ordered Item: {self.item_name}\n'
              f'Item Price: {self.price} \n'
              f'Quantity: {self.quantity} \n'
              f'Total Amount: {self.total} \n')

    def __str__(self):
        return f"Item: {self.item_name}, Category: {self.category} "

    def __repr__(self):
        return self.__str__()


class Stock:
    """Class representing the available stock from a restaurant
    It contains the quantities for each item on the menu"""
    def __init__(self) -> None:
        self.inventory={}

    def add_stock(self,item_name, quantity):
        """Add an item or increment its quantity"""

        if item_name in self.inventory:
            self.inventory[item_name] += 1
        else:
            self.inventory[item_name]=quantity


    def deduct_item(self, item: Item):
        """Rest the stock quantity from a ordered item"""
        item_name=item.item_name
        quantity=item.quantity

        if item_name in self.inventory:
            # if available
            if self.inventory[item_name] >= quantity:
                self.inventory[item_name] -= quantity
                print(f"{quantity} units of {item_name} deducted from stock.")

                # Delete the item from stock if item quantity is cero
                if self.inventory[item_name] == 0:
                    del self.inventory[item_name]
            else:
                print(f"Not enough {item_name} in stock. Available: {self.inventory[item_name]}")
        else:
            print(f"{item_name} not in stock.")


class Order:
    """Class representing the order for a lis of item from the menu"""
    #initializing the uniques id's
    _id_counter = 1
    def __init__(self, customer: Customer) -> None:
        self._order_id = Order._id_counter
        Order._id_counter+=1
        self.customer=customer
        self.ordered_items = []
        self.status = "Pending"  #initial order status
        self.total = 0

    @property
    def order_id(self):
        """order id getter"""
        return self._order_id

    def add_item(self, ordered_item: OrderedItem):
        """adds and ordered item to the order"""
        self.ordered_items.append(ordered_item)
        self.total += ordered_item.calculate_total()

    def calculate_total(self):
        """Return the total amount of the order"""
        return sum(item.calculate_total() for item in self.ordered_items)

    def show_details(self):
        """Prints out the details for the order"""
        self.total= self.calculate_total()
        print("Order Receipt")
        print(f'Order ID: {self.order_id}\n'
              f'Customer : {self.customer.name}\n'
              f'Ordered Item: {self.ordered_items}\n'
              f'Total Amount: {self.total} \n')

    def complete_order(self):
        """Update the order status"""
        self.status='Completed'



class Payment:
    """This class handles the payments attributes for a linked order"""
    def __init__(self, order:Order, payment_type:str) -> None:
        self.order=order
        self.payment_type=payment_type
        self.status = 'Pending'

    def process_payment(self):
        """Update the payment status for the order to completed"""
        self.status = 'Paid'
        self.order.complete_order()
        print(f'Payment Status for Order ID: {self.order.order_id} is {self.status.upper()}\n')


class Delivery:
    """This class represent the delivery status for a given order """
    def __init__(self,order: Order, employee:Employee, customer:Customer) -> None:
        self.order=order
        self.employee=employee
        self.customer=customer
        self.status= 'Pending'

    def start_delivery(self):
        "Update the delivery status from Pending to In Transit"
        self.status='In Transit'
        print(f'Delivery on its way to {self.customer.address}')

    def show_delivery_details(self):
        """Shows the delivery details"""
        print(f"Order ID: {self.order.order_id}\n"
              f"Assigned Employee: {self.employee.name} Job Role: {self.employee.job_role}\n"
              f"Delivery Address: {self.customer.address}\n"
              f"Delivery Status: {self.status}\n")

    def complete_delivery(self):
        """Updates the delivery status to 'Delivered' and displays delivery details."""
        self.status='Delivered'
        self.show_delivery_details()
