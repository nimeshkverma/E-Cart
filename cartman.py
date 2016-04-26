import redis
import config
from exception import ErrorMessage
from serializer import Serializer
from redis_connection import Redis
from decorators import positive_args


class Cart(object):

    """
        Main Class for Cart, contains all functionality
    """

    def __init__(self, user_id):
        """
            Constructor for the class, initializes user_id,
            redis_connection and hash_name in redis
        """
        self.user_id = user_id
        self.redis_connection = Redis().get_connections()
        self.redis_cart_init(user_id)
        self.destroy = self.__del__

    def redis_cart_init(self, user_id):
        """
            Get or create the hash_name in redis
        """
        if not self.redis_connection.hexists(config.CART_CONFIG["hash_name"], self.user_id):
            self.redis_connection.hset(
                config.CART_CONFIG["hash_name"], self.user_id, {})

    def add(self, product_id, unit_cost, quantity=1, **extra_data_dict):
        """
            Add the product of the given product_id and unit_cost with given quantity
            Can also add extra details in the form of dictionary
        """
        cart_dict = self.__cart_dict()
        cart_dict[product_id] = self.__product_dict(
            unit_cost, quantity, extra_data_dict)
        self.redis_connection.hset(
            config.CART_CONFIG["hash_name"], self.user_id, Serializer.dumps(cart_dict))

    def get_product(self, product_id):
        """
            Return the cart details for the given product_id
        """
        cart_dict = self.__cart_dict()
        return cart_dict.get(str(product_id))

    def contains(self, product_id):
        """
            Checks whether the given product exists in the cart
        """
        cart_dict = self.__cart_dict()
        return True if cart_dict.get(str(product_id)) else False

    def get(self):
        """
            Returns all the products and their details present in the cart
        """
        return self.__cart_dict()

    def count(self):
        """
            Returns the number of types of products in the carts
        """
        return len(self.get().values())

    def find(self, product_id):
        """
            Returns product details for the given product_id from the cart
        """
        return self.get().get(str(product_id))

    def remove(self, product_id):
        """
            Removes the product from the cart
        """
        cart_dict = self.__cart_dict()

        if product_id in cart_dict:
            del cart_dict[product_id]
            self.redis_connection.hset(
                config.CART_CONFIG["hash_name"], self.user_id, Serializer.dumps(cart_dict))
            return True
        else:
            return False

    def __quantities(self):
        return map(lambda product: product.get('quantity'), self.__cart())

    def quantity(self):
        """
            Returns the total number of units of all products in the cart
        """
        return reduce(lambda result, quantity: quantity + result, self.__quantities())

    def total_cost(self):
        """
            Return the net total of all product cost from the cart
        """
        return sum(self.__price_list())

    def copy(self, target_user_id):
        """
            Copies the cart of the user to the target_user_id
        """
        cart_string = self.redis_connection.hget(
            config.CART_CONFIG["hash_name"], self.user_id)
        self.redis_connection.hset(
            config.CART_CONFIG["hash_name"], target_user_id, cart_string)
        return Cart(target_user_id)

    def __cart(self):
        return self.get().values()

    def __product_price(self, product):
        return product['quantity'] * product['unit_cost']

    def __price_list(self):
        return map(lambda product: self.__product_price(product), self.__cart())

    def __del__(self):
        self.redis_connection.hdel(
            config.CART_CONFIG["hash_name"], self.user_id)

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
