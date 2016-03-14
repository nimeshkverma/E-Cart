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
