import pytest
import os, sys

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path = [os.path.join(SCRIPT_DIR + '/../../')] + sys.path

from cartman import Cart

def test_cart_should_raise_exception_without_user():
	with pytest.raises(Exception) as e_info:
		Cart()

def test_should_init_empty_cart():
    pass

