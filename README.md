# Cartman

![](http://blog.brightcove.com/sites/all/uploads/eric_theodore_cartman_southpark.jpg)

Cartman is a framework agnostic, redis backed, cart system.  It is not a POS, or a full fledged ecommerce system.  Just the cart, man.

## Installation

    pip install cartman

## Requirement
You should have running  [Redis Server](http://redis.io/topics/quickstart "Quickstart"). and installed **redis-py**  [redis-py](https://pypi.python.org/pypi/redis "Install") package.

## Usage
`from cartman import Cart`

To create a new shopping cart, just call `Cart(user_id, redis)`.  The parameter for `Cart()` is a unique id and a redis instace.  If you don't want a user to have more than one cart at a time, it's generally best to set this to the user's id.  Then to add an item to the cart, just call `cart.add(product_id, unit_cost, quantity)` which takes product_id, quantity, unit_cost and extra_product_detail(dict).  Then to retrieve the items, you just call `cart.get` which will give you a dict of all the items.

The `Cart` object also has some handy methods that you should be aware of:

- `add(product_id, unit_cost, quantity, **extra_details)` - which is the life blood of Cartman.   Here's a few suggestions of keys you may want in your hash:
  - `product_id` - (*required*) to store the ID of the model you're adding
  - `quantity` - (*required*)which will let you use the `Cart#quantity` and `Cart#total` methods without any extra configuration.
  - `unit_cost` - (*required*)which will also help to calculate total value of cart.
  - `extra_details` - (*optional*) if you want to store any extra information about the cart item just pass the dict, cartman will take care of it. 
- `remove(product_id)` - which, you guessed it, removes an item.
- `contains(product_id)` - It will tell you if a certain item is in the cart.
- `get_product(product_id)` - This will return the `Item` object that represents the object passed in.
- `get` - this returns a dict of all the items.
- `total_cost` - will sum all of the `cost` return values of all of the items in the cart.  For this to work, the `:unit_cost` and `:quantity` fields need to be set for all items.
- `count` - which will give you the total number of items in the cart.  Faster than `cart.items.size` because it doesn't load all of the item data from redis.
- `quantity` - which will return the total quantity of all the items.  The quantity field is set in the config block, by default it's `:quantity`
- `get_ttl` - will tell you how many seconds until the cart expires.
- `set_ttl` - which will reset the ttl back to whatever expiration length is set in the config.  Touch is automatically called after `add` and `remove`.
- `destroy!` - which will delete the cart, and all the line_items out of it.
- `copy(new_id)` - this method will copy the current cart to the new unique_id. Will be useful for copying guest user's cart to logged-in user's cart.

Lets walk through an example below:

```python
# app/models/user.rb
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
