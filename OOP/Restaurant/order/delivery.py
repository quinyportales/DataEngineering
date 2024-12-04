"""Module Contains Delivery class"""
from employee_and_customer.customer import Customer
from employee_and_customer.employee import Employee
from order.order_class import Order


class Delivery:
    """Models a delivery from an order in a restaurant system."""

    def __init__(self,order: Order, employee:Employee, customer:Customer) -> None:
        """
        Initialize a Delivery instance.

        Parameters:
        order: Order - An instance from the order class.
        employee:Employee - An instance from the Employee class.
        customer:Customer - An instance from the Customer class.
        """
        self.order: Order = order
        self.employee: Employee = employee
        self.customer: Customer = customer
        self.status: str = 'Pending'

    def start_delivery(self) -> None:
        "Update the delivery status from Pending to In Transit"
        self.status='In Transit'
        print(f'Delivery on its way to {self.customer.address}')

    def __str__ (self) -> str:
        """returns the string representation for Delivery instances"""
        return(f"Order ID: {self.order.order_id}\n"
              f"Assigned Employee: {self.employee.name} Job Role: {self.employee.job_role}\n"
              f"Delivery Address: {self.customer.address}\n"
              f"Delivery Status: {self.status}\n")

    def complete_delivery(self):
        """Updates the delivery status to 'Delivered' and displays delivery details."""
        self.status='Delivered'
