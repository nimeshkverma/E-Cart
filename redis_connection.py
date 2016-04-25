import redis
from decorators import singleton, raise_exception
from exception import ErrorMessage
from config import REDIS


@singleton
class Redis(object):

    @raise_exception("Redis connection can't be established due to Error: ")
    def get_connections(self):
        REDIS_SERVER = REDIS.get('SERVER')
        REDIS_PORT = REDIS.get('PORT')
        if REDIS_SERVER and REDIS_PORT:
            REDIS_DB = REDIS['DB'] if REDIS.get('DB') else 0
            REDIS_PASSWORD = REDIS['PASSWORD'] if REDIS.get(
                'PASSWORD') else None
            redis_connection = redis.Redis(
                host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
            return redis_connection
        else:
            raise ErrorMessage("REDIS_SERVER or REDIS_PORT not provided")
