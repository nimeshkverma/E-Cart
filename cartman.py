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
        self.destroy = self.__del__

    def redis_cart_init(self, user_id):
        if not self.redis_connection.hexists(config.CART_CONFIG["hash_name"], self.user_id):
            self.redis_connection.hset(
                config.CART_CONFIG["hash_name"], self.user_id, {})

    def __cart_dict(self):
        cart_string = self.redis_connection.hget(
            config.CART_CONFIG["hash_name"], self.user_id)
        return Serializer.loads(cart_string)

    def __product_dict(self, unit_cost, quantity, extra_data_dict):
        product_dict = {
            "unit_cost": unit_cost,
            "quantity": quantity
        }
        if extra_data_dict:
            product_dict.update(extra_data_dict)
        return product_dict

    def add(self, product_id, unit_cost, quantity=1, **extra_data_dict):
        cart_dict = self.__cart_dict()
        cart_dict[product_id] = self.__product_dict(
            unit_cost, quantity, extra_data_dict)
        self.redis_connection.hset(
            config.CART_CONFIG["hash_name"], self.user_id, Serializer.dumps(cart_dict))

    def get_product(self, product_id):
        cart_dict = self.__cart_dict()
        return cart_dict.get(str(product_id))

    def contains(self, product_id):
        cart_dict = self.__cart_dict()
        return True if cart_dict.get(str(product_id)) else False

    def get(self):
        cart_dict = self.__cart_dict()
        return cart_dict

    def remove(self, product_id):
        cart_dict = self.__cart_dict()
        if product_id in cart_dict:
            del cart_dict[product_id]
            self.redis_connection.hset(
                config.CART_CONFIG["hash_name"], self.user_id, Serializer.dumps(cart_dict))
            return True
        else:
            return False

    def __product_price(self, product):
        return product['quantity'] * product['unit_cost']

    def __price_list(self):
        return map(lambda product: self.__product_price(product), self.get().values())

    def total_cost(self):
        return sum(self.__price_list())

    def __del__(self):
        self.redis_connection.hdel(
            config.CART_CONFIG["hash_name"], self.user_id)
