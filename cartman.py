import redis
import config
from serializer import Serializer
from redis_connection import Redis


class Cart(object):

    """docstring for Cart"""

    def __init__(self, user_id):
        # Init function to check weather the cart dictionary exists in redis
        # this can also be done via user every time he uses the library
        self.user_id = user_id
        self.redis_connection = Redis().get_connections()
        self.redis_cart_init(user_id)

    def redis_cart_init(self, user_id):
        if not self.redis_connection.hexists(config.CART_CONFIG["hash_name"], self.user_id):
            self.redis_connection.hset(
                config.CART_CONFIG["hash_name"], self.user_id, {})

    def __cart_dict(self):
        cart_string = self.redis_connection.hget(
            config.CART_CONFIG["hash_name"], self.user_id)
        return Serializer.loads(cart_string)

    def __product_dict(self, product_price, qty, extra_data_dict):
        product_dict = {
            "product_price": product_price,
            "qty": qty
        }
        if extra_data_dict:
            product_dict.update(extra_data_dict)
        return product_dict

    def add(self, product_id, product_price, qty=1, **extra_data_dict):
        cart_dict = self.__cart_dict()
        cart_dict[product_id] = self.__product_dict(
            product_price, qty, extra_data_dict)
        self.redis_connection.hset(
            config.CART_CONFIG["hash_name"], self.user_id, Serializer.dumps(cart_dict))

    def get(self, product_id):
        cart_dict = self.__cart_dict()
        return cart_dict.get(str(product_id))

    def remove(self, product_id):
        cart_dict = self.__cart_dict()
        if product_id in cart_dict:
            del cart_dict[product_id]
            self.redis_connection.hset(
                config.CART_CONFIG["hash_name"], self.user_id, Serializer.dumps(cart_dict))
            return True
        else:
            return False
