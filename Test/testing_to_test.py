import requests
from datetime import datetime


def even_odd(x):
    """Checks number if it even or odd.

    Args:
        x (int): number to check.

    Returns:
        str: result of check. `even` if given number is even
            and `odd` if the number is odd.
    """
    if (x % 2 == 0):
        return "even"
    else:
        return "odd"


def sum_all(*numbers):
    """Sums all given numbers together.

    Args:
        *args (int or float): variable length argument list.


    Returns:
        int or float: the result of adding all numbers together.
    """
    result = 0
    for num in numbers:
        result += num
    return result


def time_of_day():
    """Identifies current time of day.

    Returns:
        str: current time of day. Could be: "night", "morning", "afternoon".
    """
    now = datetime.now()
    if now.hour >= 0 and now.hour < 6:
        return "night"
    if now.hour >= 6 and now.hour < 12:
        return "morning"
    if now.hour >= 12 and now.hour < 18:
        return "afternoon"
    return "night"


class Product:
    """Data class representation of a product in a shop.

    Args:
        title (str): title of the product
        price (float): price of one product
        quantity (int, optional): the amount of the product available.
            Defaults to 1
    """

    def __init__(self, title, price, quantity=1):
        self.title = title
        self.quantity = quantity
        self.price = price

    def subtract_quantity(self, num_of_products=1):
        """Subtracts the number of available products.

        Args:
            num_of_products (int, optional): number of products
                available to subtract. Defaults to 1.
        """
        self.quantity -= num_of_products

    def add_quantity(self, num_of_products=1):
        """Adds the number of available products.

        Args:
            num_of_products (int, optional): number of products
                available to add. Defaults to 1.
        """
        self.quantity += num_of_products

    def change_price(self, new_price):
        """Changes price of one product.

        Args:
            new_price (float): the price to change to.
        """
        self.price = new_price


class Shop:
    """Representation of the shop

    Args:
        products (list or Product, optional): products to add to a shop while creating it.
    """

    def __init__(self, products=None):
        if products is None:
            products = []
        elif isinstance(products, Product):
            products = [products]
        self.products = products
        self.money = .0

    def add_product(self, product):
        """Adds product to the shop.

        Args:
            product (Product): product to add to the shop.
        """
        self.products.append(product)

    def _get_product_index(self, product_title):
        """Looks for products in the shop.

        Args:
            product_title (str): title of the product to look for.

        Returns:
            int: the index of the product if it present in the shop else None
        """
        for index, product in enumerate(self.products):
            if product.title == product_title:
                return index
        return None

    def sell_product(self, product_title, qty_to_sell=1):
        """Sells product and returns the final money amount to pay.

        Args:
            product_title (str): the title of the product to sell.
            qty_to_sell (int, optional): the quantity of the product to sell.
                Defaults to 1.

        Raises:
            ValueError: in case if amount of available products
                of that type is less then given.

        Returns:
            float: money amount to pay.
        """
        product_index = self._get_product_index(product_title)
        receipt = .0
        if product_index is not None:
            if self.products[product_index].quantity < qty_to_sell:
                raise ValueError('Not enough products')
            else:
                receipt = self.products[product_index].price * qty_to_sell
                if self.products[product_index].quantity == qty_to_sell:
                    del self.products[product_index]
                else:
                    self.products[product_index].subtract_quantity(qty_to_sell)
                self.money += receipt
            return receipt


def get_book_price(book_id):  # don't test this func, test next one calling it instead
    response = requests.get(f"https://example.com/book_prices/{book_id}")
    if response.status_code == 200:
        return float(response.text)


def calculate_total_textbook_cost(book_ids): #use mocker here to mock previous function call
    total_cost = 0.0
    for book_id in book_ids:
        price = get_book_price(book_id)
        if price is not None:
            total_cost += price
    return total_cost
