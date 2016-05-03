# Cartman

![](http://blog.brightcove.com/sites/all/uploads/eric_theodore_cartman_southpark.jpg)

Cartman is a framework agnostic, redis backed, cart system, built in Python.
It is not a POS, or a full fledged ecommerce system.  Just the *Cart, Man!*

## Installation

    pip install cartman

## Requirement
You should have running  [Redis Server](http://redis.io/topics/quickstart "Quickstart"). and installed **redis-py**  [redis-py](https://pypi.python.org/pypi/redis "Install") package.

## Usage

- Import the `Cart` class from the `cartman` package:

    `from cartman import Cart`

- Create a new shopping cart:

    `cart_obj = Cart(user_id, redis_connection, ttl)`
    
    `user_id` : This a required parameter which acts as a unique identifier for the cart. If you don't want a user to have more than one cart at a time, it's generally best to set this to the user's id.
    
    `redis_connection`: This too is a required field and is used to communicate with the Redis database. This is basically a  redis connection object obtained by calling the `redis.Redis()` function of the [redis package](https://redis-py.readthedocs.io/en/latest/). An sample function to create such object is available at [redis_connection.py](https://github.com/nimeshkverma/cartman/blob/master/redis_connection.py)
    
    `ttl`: This field used to set the expiry time of the user cart in the Redis in seconds. This is an optional field with a default value of 604800.

- To add an item to the cart:

    `cart_obj.add(product_id, unit_cost, quantity)`
    
    This function take `product_id`, `unit_cost` and `quantity` and other details (`**kwargs`) if you like. Once executed this function add the given product and its deatails into the user cart in redis db.
    
- To Retrieve the items:

   `cart_obj.get()`

    This function returns the complete cart of the user, basically a dictionary of product_id to product_details dictionary.
    

Following are the complete details of the methods exposed by `cart_obj` object:

- *add*

    `add(product_id, unit_cost, quantity, **extra_details)`

    This function is the life blood of Cartman. Below are the details of the arguments for the *add* function:
    - `product_id`: (*required*) to store the ID of the model you're adding
    - `quantity`: (*required*) which will let you use the `Cart#quantity` and `Cart#total` methods without any extra configuration.
    - `unit_cost`: (*required*) which will help you to calculate total value of cart.
    - `extra_details`:(*optional*) if you want to store any extra information about the cart item just pass the details as **kwargs, cartman will take care of it. 

- *remove*
    
    `remove(product_id)`

    As you would have guessed, removes an item of the input `product_id`

- *contains*

    `contains(product_id)`
    
    Returns a Boolean indicating whether an item of the given `product_id` is in the cart or not.

- *get_product*

    `get_product(product_id)`
    
    For the input `product_id`, this function will return the `Item` dictionary with `unit_cost`, `quantity` etc details.

- *get*
    
    `get()`

    This function returns the complete cart of the user, basically a dictionary of product_id to product_details dictionary.

- *total_cost*

    `total_cost()`
    
    This will return the sum all of the `cost` return values of all of the items in the cart.  For this to work, the `:unit_cost` and `:quantity` fields need to be set for all items.

- *count*

    `count()`
    
    This will return the total number of items in the cart.  Faster than `cart.items.size` because it doesn't load all of the item data from redis.

- *quantity*

    `quantity()`
    
    This will return the total quantity of all the items.  The quantity field is set in the config block, by default it's `:quantity`

- *get_ttl*

    `get_ttl()`
    
    This will return the number of seconds until the cart expires.

- *set_ttl*

    `set_ttl(ttl_value)`
    
    This will set the ttl of the user cart in redis to `ttl_value`. `ttl_value` must be integer and is in seconds

- *destroy*

    `destroy()`
    
    This will delete the cart, and all the line_items out of it.

- *copy*

    `copy(new_id)`
    
    This method will copy the current cart to the new unique_id. Will be useful for copying guest user's cart to logged-in user's cart or simply creating a copy of the cart.
    
Lets walk through an example below:

```python
from cartman import Cart
cart = Cart(user_id, reddis_connection) # ttl is optional default is 604800
cart.add(product_id, unit_cost, quantity) # quantity defaults to 1, also you can pass optional dict(extra info)
cart.total
cart.quantity
```


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
