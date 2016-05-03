import redis
from decorators import singleton, raise_exception
from exception import ErrorMessage


@singleton
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
