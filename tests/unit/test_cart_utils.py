import os, sys
import pytest

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path = [os.path.join(SCRIPT_DIR + '/../../')] + sys.path

from cartman import Cart

@pytest.fixture(scope='function')
def cart():
    c = Cart(123)
    qty = 2
    price = 12
    c.add(12, price, qty)
    return c

def test_should_return_valid_total(cart):
    assert 24 == cart.total_cost()

def test_should_not_return_valid_total(cart):
    assert 214 != cart.total_cost()
