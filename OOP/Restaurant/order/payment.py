"""Module Contains Payment class"""
from .order_class import Order


class Payment:
    """This class handles the payment process for an order, 
    including the payment type and status."""

    def __init__(self, order:Order, payment_type:str) -> None:
        """
        Initialize a Customer instance.

        Parameters:
        order: Order - An instance of class Order
        """
        self.order: Order = order
        self.payment_type: str = payment_type
        self.status: str = 'Pending'

    def process_payment(self) -> None:
        """Update the payment status for the order to completed"""
        self.status: str = 'Paid'
        self.order.complete_order()
        print(f'Payment Status for Order ID: {self.order.order_id} is {self.status.upper()}\n')
