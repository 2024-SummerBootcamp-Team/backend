import redis

class Config:
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None
    REDIS_DB = 0

    @staticmethod
    def get_redis_client():
        return redis.StrictRedis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            db=Config.REDIS_DB
        )