import redis
from functools import wraps


class ErrorMessage(Exception):

    def __init__(self, msg):
        self.value = msg

    def __str__(self):
        return repr(self.value)


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


class Redis(object):

    @raise_exception("Redis connection can't be established due to Error: ")
    def get_connections(self, host, port, db=0, password=None):
        REDIS_SERVER = host
        REDIS_PORT = port
        if REDIS_SERVER and REDIS_PORT:
            REDIS_DB = db
            REDIS_PASSWORD = password
            redis_connection = redis.Redis(
                host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
            return redis_connection
        else:
            raise ErrorMessage("REDIS_SERVER or REDIS_PORT not provided")
