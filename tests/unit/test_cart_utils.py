import os, sys
import pytest

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path = [os.path.join(SCRIPT_DIR + '/../../')] + sys.path

from cartman import Cart

qty = 2
price = 10
product_id = 12

@pytest.fixture(scope='function')
def cart():
    c = Cart(123)
    c.add(product_id, price, qty)
    return c

def test_valid_price_list(cart):
    assert cart._Cart__price_list() == [20]

def test_invalid_price_list(cart):
    assert cart._Cart__price_list() != [20, 10]

def test_should_return_valid_total(cart):
    assert 20 == cart.total_cost()

def test_should_not_return_valid_total(cart):
    assert 214 != cart.total_cost()

def test_valid_product_price(cart):
    assert cart._Cart__product_price(cart.find(product_id)) == 20

def test_invalid_product_price(cart):
    assert cart._Cart__product_price(cart.find(product_id)) != 21

def test_count(cart):
    assert cart.count() == 1

def test_invalid_count(cart): 
    assert cart.count() != 2

def test_quantity(cart):
    assert cart.quantity() == 2
