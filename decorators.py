import json
from functools import wraps
from exception import ErrorMessage


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


def raise_exception(msg_prefix='', *args, **kwargs):
    def deco(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                msg = msg_prefix + str(e)
                raise ErrorMessage(msg)
        return decorated_function
    return deco


def positive_args(f):
    def check_positivity(arg_value):
        if type(arg_value) in [int, float] and arg_value <= 0:
            raise ErrorMessage("Arguments must have value greater than 0")

    @wraps(f)
    def decorated_function(*args, **kwargs):
        for arg in args + kwargs.values():
            check_positivity(arg)
