"""Test class Product for testing_to_test module"""
import pytest
from testing_to_test import Product

def test_product_initialization_positive(product_fixture : Product) -> None:
    """Test the Product class initialization with valid values"""
    product = product_fixture
    assert product.title == 'Novel Harry Potter'
    assert product.price == 12500.50
    assert product.quantity == 5

@pytest.mark.xfail(reason="Product initialization isn't managing the invalid inputs") 
@pytest.mark.parametrize('title, price, quantity, expected_error',
                         [(None, 2000.0, 5, TypeError), #invalid title
                         ('Novel Harry Potter', -2000.0, 5, ValueError), #invalid price
                         ('Novel Harry Potter', 2000.0, -5, ValueError)]) #invalid quantity

def test_product_initialization_negatives(title: str, 
                                          price: float, 
                                          quantity: int, 
                                          expected_error: type) -> None:
    """Test the Product class initialization with invalid values"""
    #the class is not handling the invalid cases
    try:
        Product(title, price, quantity)
    except expected_error:
        #Here we are expected that the exception be implemented by the code
        pass
    else:
        # if the exception is not raised
        pytest.fail(f"Expected TypeError, but no exception was raised"
            f"when initializing Product using {title} {price} {quantity}")

@pytest.mark.xfail(reason="Product subtract_quantity method isn't managing the invalid inputs") 
@pytest.mark.parametrize(
    "initial_qty, num_to_subtract, expected_qty, should_raise",
    [
        (5, 3, 2, False),  # standar case
        (5, 6, None, True),  # subtracting more than available
        (5, 5, 0, False),  # subtracting all
        (5, 0, 5, False)  # subtracting cero
        ])
def test_subtract_quantity(initial_qty: int, 
                           num_to_subtract: int, 
                           expected_qty: int, 
                           should_raise: bool, 
                           product_fixture: Product) -> None:
    """Test different scenarios for subtracting_quantity method from Product class.
    should_raise == True 
    if an Exception/Error must be raised for a specific case"""
    product = product_fixture
    product.quantity = initial_qty

    if should_raise:
        try:
            product.subtract_quantity(num_to_subtract)
        except ValueError:
            #Expected exception, so nothing to do here
            pass
        else:
            # if the exception is not raised
            pytest.fail("Expected ValueError when using subtract_quantity " 
                                 f"but no exception was raised when using {initial_qty}-{num_to_subtract}")
    else:
        product.subtract_quantity(num_to_subtract)
        assert product.quantity == expected_qty

@pytest.mark.xfail(reason="Product add_quantity method isn't managing the invalid inputs") 
@pytest.mark.parametrize ("initial_qty, num_to_add, expected_qty,should_raise",
                          [
                              (5, 3, 8, False), #standar case
                              (0, 3, 3, False), #adding to cero qty
                              (5, 0, 5, False), #adding cero
                              (5, -6, None, True) #adding negative qty
                              ])
def test_add_quantity(initial_qty: int, 
                      num_to_add: int, 
                      expected_qty: int, 
                      should_raise: bool, 
                      product_fixture: Product ) -> None:
    """Test different scenarios for adding_quantity method from Product class.
    should_raise == True if an Exception/Error must be raised for a specific case"""
    product = product_fixture
    product.quantity = initial_qty

    if should_raise:
        try:
            product.add_quantity(num_to_add)
        except ValueError:
            #Here we are expecting that the exception be implemented by the code
            pass
        else:
            # if the exception is not raised
            pytest.fail("Expected ValueError when using  add_quantity"
            f"but no exception was raised when using {initial_qty} + {num_to_add}")
    else:
        product.add_quantity(num_to_add)
        assert product.quantity == expected_qty


@pytest.mark.xfail(reason="Product change_price method isn't managing the invalid inputs") 
@pytest.mark.parametrize("initial_price, new_price, expected_price, should_raise",
                         [(12500.50, 10000.0, 10000.0, False), #standar case valid value
                            (12500.50, 0, 0, False), #price cero
                            (12500.50, -12500.0, 0, True), #negative price
                            ])
def test_change_price(initial_price: float, 
                      new_price: float, 
                      expected_price: float, 
                      should_raise: bool, 
                      product_fixture: Product) -> None:
    """Test different scenarios for change_price method from Product class.
    should_raise == True if an Exception/Error must be raised for a specific case"""

    product = product_fixture
    product.price = initial_price

    if should_raise:
        try:
            product.change_price(new_price)
        except ValueError:
        #Here we are expecting that the exception be implemented by the code
            pass
        else:
            #if the exception is not raised
            pytest.fail("Expected ValueError when using  change_price"
            f"but no exception was raised when using {initial_price} to {new_price}")
    else:
        product.change_price(new_price)
        assert product.price == expected_price
