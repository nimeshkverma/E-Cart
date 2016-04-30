import redis
import copy
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
            Constructor for the class, initializes user_id and checks whether
            the users' cart exists or not.
        """
        self.user_id = user_id
        self.user_redis_key = __get_user_redis_key(user_id)
        self.redis_connection = Redis().get_connections()
        self.redis_user_hash_token = "CARTMAN"
        self.user_cart_exists = self.cart_exists(user_id)
        self.destroy = self.__del__

    def __cart_dict(self):
        cart_string = self.redis_connection.hget(
            config.CART_CONFIG["hash_name"], self.user_id)
        return Serializer.loads(cart_string)

    def __product_dict(self, unit_cost, quantity, extra_data_dict):
        """
            Returns the dictionary for a product, with the argument values.
        """
        product_dict = {
            "unit_cost": unit_cost,
            "quantity": quantity
        }
        product_dict.update(extra_data_dict)
        return product_dict

    def cart_exists(self, user_id):
        """
            Confirm user's cart hash in Redis
        """
        return self.redis_connection.exists(get_user_redis_key(self.user_id))

    def __get_user_redis_key_prefix():
        """
            Generate the prefix for the user's redis key. 
        """
        return ":".join([config.REDIS_USER_PREFIX, self.redis_user_hash_token, "USER_ID"])

    def __get_user_redis_key(self, user_id):
        """
            Generates the name of the Hash used for storing User cart in Redis
        """
        if user_id:
            return __get_user_redis_key_prefix() + ":"+str(user_id)
        else:
            raise ErrorMessage("user_id can't be null")

    def get_user_redis_key(self):
        """
            Returns the name of the Hash used for storing User cart in Redis
        """
        return self.user_redis_key

    def add(self, product_id, unit_cost, quantity=1, **extra_data_dict):
        """
            Returns True if the addition of the product of the given product_id and unit_cost with given quantity 
            is succesful else False.
            Can also add extra details in the form of dictionary.
        """
        product_dict = self.self.__product_dict(
            unit_cost, quantity, extra_data_dict)
        is_added = self.redis_connection.hset(
            self.user_redis_key, product_id, Serializer.dumps(product_dict))
        if not self.user_cart_exists and is_added:
            self.user_cart_exists = True
        return True if is_added else False

    def get_product(self, product_id):
        """
            Return the cart details as a Dictionary for the given product_id
        """
        if self.user_cart_exists:
            product_string = self.redis_connection.hget(
                self.user_redis_key, str(product_id))
            if product_string:
                return Serializer.loads(product_string)
            else:
                return {}
        else:
            raise ErrorMessage("The user cart is Empty")

    def contains(self, product_id):
        """
            Checks whether the given product exists in the cart
        """
        return self.redis_connection.hexists(self.user_redis_key, str(product_id))

    def get(self):
        """
            Returns all the products and their details present in the cart as a dictionary
        """
        cart_string = self.redis_connection.hgetall(self.user_redis_key)
        return {key: Serializer.loads(value) for key, value in cart_string.iteritems()}

    def count(self):
        """
            Returns the number of types of products in the carts
        """
        return self.redis_connection.hlen(self.user_redis_key)

    def remove(self, product_id):
        """
            Removes the product from the cart
        """
        if self.user_cart_exists:
            if self.redis_connection.hdel(self.user_redis_key, str(product_id)):
                return True
            else:
                return False
        else:
            raise ErrorMessage("The user cart is Empty")

    def __quantities(self):
        return map(lambda product_dict: product_dict.get('quantity'), self.get().values())

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
        cart_string = self.redis_connection.hgetall(self.user_redis_key)
        is_copied = self.redis_connection.hset(
            self.__get_user_redis_key(target_user_id), cart_string)
        return True if is_copied else False

    def __product_price(self, product):
        """
            Return the product of product_quantity and its unit_cost
        """
        return product['quantity'] * product['unit_cost']

    def __price_list(self):
        """
            Returns the list of product's total_cost
        """
        return map(lambda product_dict: self.__product_price(product), self.get().values())

    def __del__(self):
        """
            Deletes the user's cart
        """
        self.redis_connection.delete(self.user_redis_key)
