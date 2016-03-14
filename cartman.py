import redis
import config
from serializer import Serializer
from redis_connection import RedisConnection


class Cart(object):

    """docstring for Cart"""

    def __init__(self, user_id):
        # Init function to check weather the cart dictionary exists in redis
        # this can also be done via user every time he uses the library
        self.user_id = user_id
        self.redis_cart_init(user_id)

    def redis_cart_init(self, user_id):
        if not RedisConnection.hexists(config.CART_CONFIG["hash_name"], self.user_id):
            RedisConnection.hset(
                config.CART_CONFIG["hash_name"], self.user_id, {})

    def __cart_dict(self):
        cart_string = RedisConnection.hget(
            config.CART_CONFIG["hash_name"], self.user_id)
        return Serializer.loads(cart_string)

    def __product_dict(self, product_price, qty, **kwargs):
        return {
            "product_price": product_price,
            "qty": qty
        }.update(kwargs)

    def add(self, product_id, product_price, qty=1, **kwargs):
        cart_dict = self.__cart_dict()
        cart_dict[product_id] = self.__product_dict(product_id, qty, kwargs)
        RedisConnection.hset(
            config.CART_CONFIG["hash_name"], self.user_id, Serializer.dumps(cart_dict))

    def remove(self, product_id):
        pass
