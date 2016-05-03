# Cartman

![](http://blog.brightcove.com/sites/all/uploads/eric_theodore_cartman_southpark.jpg)

Cartman is a framework agnostic, redis backed, cart system, built in Python.
It is not a POS, or a full fledged ecommerce system.  Just the *Cart, Man!*

## Installation

    pip install cartman

## Requirement
You should have running  [Redis Server](http://redis.io/topics/quickstart "Quickstart"). and installed **redis-py**  [redis-py](https://pypi.python.org/pypi/redis "Install") package.

## Basic Usage

1. Import the `Cart` class from the `cartman` package:

    `from cartman import Cart`

2. Create a new shopping cart:

    `cart_obj = Cart(user_id, redis_connection, ttl)`
    
    `user_id` : This a required parameter which acts as a unique identifier for the cart. If you don't want a user to have more than one cart at a time, it's generally best to set this to the user's id.
    
    `redis_connection`: This too is a required field and is used to communicate with the Redis database. This is basically a  redis connection object obtained by calling the `redis.Redis()` function of the [redis package](https://redis-py.readthedocs.io/en/latest/). An sample function to create such object is available at [redis_connection.py](https://github.com/nimeshkverma/cartman/blob/master/redis_connection.py)
    
    `ttl`: This field used to set the expiry time of the user cart in the Redis in seconds. This is an optional field with a default value of 604800.

3. To add an item to the cart:

    `cart_obj.add(product_id, unit_cost, quantity)`
    
    This function take `product_id`, `unit_cost` and `quantity` and other details (`**kwargs`) if you like. Once executed this function add the given product and its deatails into the user cart in redis db.
    
4. To Retrieve the items:

   `cart_obj.get()`

    This function returns the complete cart of the user, basically a dictionary of product_id to product_details dictionary.
    
## Functions Exposed

Following are the complete details of the methods exposed by `cart_obj` object:

- **_add_**

    `add(product_id, unit_cost, quantity, **extra_details)`

    This function is the life blood of Cartman. Below are the details of the arguments for the *add* function:
    - `product_id`: (*required*) to store the ID of the model you're adding
    - `quantity`: (*required*) which will let you use the `Cart#quantity` and `Cart#total` methods without any extra configuration.
    - `unit_cost`: (*required*) which will help you to calculate total value of cart.
    - `extra_details`:(*optional*) if you want to store any extra information about the cart item just pass the details as **kwargs, cartman will take care of it. 

- **_remove_**
    
    `remove(product_id)`

    As you would have guessed, removes an item of the input `product_id`

- **_contains_**

    `contains(product_id)`
    
    Returns a Boolean indicating whether an item of the given `product_id` is in the cart or not.

- **_get_product_**

    `get_product(product_id)`
    
    For the input `product_id`, this function will return the `Item` dictionary with `unit_cost`, `quantity` etc details.

- **_get_**
    
    `get()`

    This function returns the complete cart of the user, basically a dictionary of product_id to product_details dictionary.

- **_total_cost_**

    `total_cost()`
    
    This will return the sum all of the `cost` return values of all of the items in the cart.  For this to work, the `:unit_cost` and `:quantity` fields need to be set for all items.

- **_count_**

    `count()`
    
    This will return the total number of items in the cart.  Faster than `cart.items.size` because it doesn't load all of the item data from redis.

- **_quantity_**

    `quantity()`
    
    This will return the total quantity of all the items.  The quantity field is set in the config block, by default it's `:quantity`

- **_get_ttl_**

    `get_ttl()`
    
    This will return the number of seconds until the cart expires.

- **_set_ttl_**

    `set_ttl(ttl_value)`
    
    This will set the ttl of the user cart in redis to `ttl_value`. `ttl_value` must be integer and is in seconds

- **_destroy_**

    `destroy()`
    
    This will delete the cart, and all the line_items out of it.

- **_copy_**

    `copy(new_id)`
    
    This method will copy the current cart to the new unique_id. Will be useful for copying guest user's cart to logged-in user's cart or simply creating a copy of the cart.

##Example

Lets walk through an example below:

```python
from cartman import Cart
cart = Cart(user_id, reddis_connection) # ttl is optional default is 604800
cart.add(product_id, unit_cost, quantity) # quantity defaults to 1, also you can pass optional dict(extra info)
cart.total
cart.quantity
```


## How to Contribute

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
