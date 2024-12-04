"""Test class Shop for testing_to_test module"""
import pytest
from testing_to_test import Product, Shop

def test_shop_initialization_positive(shop_fixture: Shop) -> None:
    """Test the Shop class initialization with a predefined set of products.

    Validates that the `Shop` instance is created with the correct number of 
    products, and each product has the expected title, price, and quantity. 
    Also checks that the initial money in the shop is set to 0.
    """

    shop = shop_fixture
    
    # Assert that shop has the correct number of products
    assert len(shop.products) == 3

    # Assert that products have correct details
    assert shop.products[0].title == 'Novel The lord of the rings'
    assert shop.products[0].price == 20000.0
    assert shop.products[0].quantity == 2

    assert shop.products[1].title == 'Novel Farenheit 451'
    assert shop.products[1].price == 5000.0
    assert shop.products[1].quantity == 1

    assert shop.products[2].title == 'Novel One Hundred Years of Solitude'
    assert shop.products[2].price == 25000.0
    assert shop.products[2].quantity == 10

    # Assert that the initial money is 0
    assert shop.money == 0.0


def test_shop_initialization_empty() -> None:
    """Test the Shop class initialization with an empty product list.

    Ensures that an instance of `Shop` created without any products 
    initializes correctly with an empty list and money set to 0.
    """

    shop = Shop()

    #assert that products is an empty list
    assert shop.products == []
    assert shop.money == 0.0

def test_shop_initialization_single_product(product_fixture: Product) -> None:
    """Test the Shop class initialization with a single product.

    Verifies that a `Shop` instance is correctly initialized when given a 
    single `Product` instance, and ensures the product's attributes are accurate.
    """
    shop = Shop(product_fixture)

    #assenting that product list only contains one product
    assert len(shop.products) == 1

    #asserting that attributes are right
    assert shop.products[0].title == 'Novel Harry Potter'
    assert shop.products[0].price == 12500.50
    assert shop.products[0].quantity == 5


#testing with invalid data
@pytest.mark.xfail(reason="Shop isn't managing the invalid inputs") 
@pytest.mark.parametrize('input_value, should_raise', [
    ('Not a list nor a Product instance', True), #testing with invalid data
    (None, True), #testing with explicit none
    ])
def test_shop_initialization_negative(input_value: str, should_raise: bool):
    """Test the Shop class initialization with invalid inputs.

    This test checks the behavior of the `Shop` constructor when given 
    invalid inputs, such as `None` or a non-`Product` type. Ensures that 
    appropriate exceptions (`TypeError`) are raised.
    """
    if should_raise:
        try:
            Shop(input_value)
            pytest.fail(f"Expected TypeError, but no exception was raised "
            f"when initializing Shop using {input_value}")
        except TypeError:
            #Here we are expecting that the exception be implemented by the code
                pass
        except Exception as e:
            #if a different exception type is raised
            pytest.fail(f"Expected TypeError, but {type(e.__name__)} was raised instead"
            f"when initializing Shop using {input_value}")
    else:
        shop = Shop(input_value)
        assert shop.products == []


@pytest.mark.xfail(reason="Shop add_product method isn't managing the invalid inputs") 
@pytest.mark.parametrize('invalid_product, expected_error', [
    # negative price 
    (Product('Invalid Product 1', -5000.0, 5), ValueError),  

    #negative quantity
    (Product('Invalid Product 2', 1000.0, -2), ValueError),

    #not a Product instance
    (('Not a Product', 1000, 1), TypeError),

    #None product value
    ((None, None, None), TypeError),
])
def test_add_product(invalid_product: tuple[str, float, int], 
    expected_error: type[Exception], 
    product_fixture: Product, 
    shop_fixture: Shop):
    """Test the add_product method of the Shop class.

    - Validates that a valid `Product` instance is correctly added to the shop.
    - Checks for appropriate errors when invalid inputs are passed, such as:
      - Products with negative price or quantity.
      - Non-`Product` objects.
      - `None` values.
    """

    #testing the standard case
    shop = shop_fixture
    shop.add_product (product_fixture)

    assert shop.products[-1] == product_fixture

    #testing the negative cases
    try:
        shop.add_product(invalid_product)
        
    except TypeError:
        #Here we are expected that the exception be implemented by the code
            pass
    else:
        #if the exception is not raised
        if isinstance(invalid_product, Product):
            product_details = f"title={invalid_product.title}, price={invalid_product.price}, quantity={invalid_product.quantity}"
        else:
            product_details = str(invalid_product)
        
        pytest.fail(f"Expected {expected_error.__name__}, but no exception was raised "
            f"when adding product with details: {product_details}")


@pytest.mark.parametrize('invalid_product, expected_index',[
    # Testing invalid products: None, non-existent, or empty title
    (None, None ),  
    ('Non existent book', None), 
    ('', None) 
    ])

def test_get_product_index(invalid_product : str, expected_index : int, shop_fixture : Shop):
    """Test the _get_product_index private method of the Shop class.

    - Ensures the method returns the correct index for valid product titles.
    - Verifies that invalid titles (e.g., `None`, non-existent, or empty titles) 
      return the expected index (`None`).
    """

    shop = shop_fixture
    #testing the standard case
    assert shop._get_product_index(shop.products[0].title) == 0

    #testing the invalid products
    assert shop._get_product_index(invalid_product) == expected_index



def test_sell_product_positives(shop_fixture: Shop):
    """Test selling a valid product in the Shop.

    - Verifies that selling a product reduces its quantity by the specified amount.
    - Checks that the correct receipt amount is returned for the sale.
    - Confirms that the shop's money balance is updated correctly.
    """
    #testing the standard case
    shop = shop_fixture
    product = shop_fixture.products[0]

    initial_quantity = product.quantity
    product_receipt = product.price * 1

    assert shop.sell_product(product.title, 1) == product_receipt

    # Checking if the qty was updated
    assert product.quantity == initial_quantity - 1

    # Checking if the money was updated
    assert shop.money == product_receipt


@pytest.mark.xfail(reason="Shop sell_product method isn't managing the invalid inputs") 
@pytest.mark.parametrize('product_title, qty_to_sell, expected_error, expected_receipt, expected_remaining_qty',
                         [
                             #testing non existing books and invalid quantities
                             ("Non-existent product", 1, ValueError, None, None),  # Expect ValueError if product not found
                             ("Novel Farenheit 451", 10, ValueError, None, None),  # Expect ValueError for insufficient quantity
                         ])
def test_sell_product_negatives(product_title: str, 
    qty_to_sell: int, 
    expected_error: type[Exception], 
    expected_receipt: float, 
    expected_remaining_qty: int, 
    shop_fixture: Shop) -> None :
    """Test selling invalid products or quantities in the Shop.

    - Ensures that attempting to sell a non-existent product raises a `ValueError`.
    - Verifies that selling more than the available quantity also raises a `ValueError`.
    - Checks that appropriate exception messages are returned.
    """

    shop = shop_fixture
    
    try:
        shop.sell_product(product_title, qty_to_sell)
    except expected_error as e:
        # Check if the exception message matches what is expected for ValueError
        if expected_error == ValueError:
            assert str(e) == "Not enough products"
        else:
            assert isinstance(e, expected_error)  # In case of other exceptions, just assert the type
    else:
        pytest.fail(f"Expected {expected_error}, but no exception was raised when attempting "
                             f"to sell {qty_to_sell} units of '{product_title}'")