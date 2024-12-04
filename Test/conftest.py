"""
Configuration and shared fixtures for pytest.

Fixtures:
    - product_fixture: Initializes an instance of the Product class for testing.
    - shop_fixture: Initializes an instance of the Shop class with multiple products.
"""
from itertools import product
import pytest
from testing_to_test import Product, Shop

@pytest.fixture
def product_fixture():
    """
    Fixture that initializes an instance of the Product class.

    Returns:
        Product: A product instance with preset attributes.
    """
    return Product(title='Novel Harry Potter', price= 12500.50, quantity= 5)


@pytest.fixture
def shop_fixture():
    """
    Fixture that initializes an instance of the Shop class with multiple products.

    Returns:
        Shop: A shop instance containing a preset list of products.
    """
    product1 = Product(title='Novel The lord of the rings', price= 20000.0, quantity= 2)
    product2 = Product(title='Novel Farenheit 451', price= 5000.0, quantity= 1)
    product3 = Product(title='Novel One Hundred Years of Solitude', price= 25000.0, quantity= 10)
    return(Shop([product1,product2, product3]))
