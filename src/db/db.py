import redis


class DB:
    def __init__(self) -> None:
        self.__redis = redis.Redis(host='db', port=6379, decode_responses=True)

    def get_user_points_db(self, guild_id: int, user_id: int) -> int:
        if points := self.__redis.hget(str(guild_id), str(user_id)):
            return int(points)
        return 0

    def increment_user_points_db(self, guild_id: int, user_id: int, points: int) -> None:
        self.__redis.hincrby(str(guild_id), str(user_id), points)

    def set_user_points_db(self, guild_id: int, user_id: int, points: int) -> None:
        self.__redis.hset(str(guild_id), str(user_id), str(points))