import pytest
import os, sys

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path = [os.path.join(SCRIPT_DIR + '/../../')] + sys.path

from cartman import Cart

def test_should_throw_error_without_config():
	# os.rename("config.py", "config1.py")
		# os.rename("config1.py", "config.py")
		Cart(12)

def test_cart_should_raise_exception_without_user():
	with pytest.raises(Exception) as e_info:
		Cart()


