import redis

class Idb:
    def __init__(self):
        self.__redis = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )

    def get_user_points_form_db(self, id_user: int, id_guild: int):
        if user := self.__redis.hgetall(str(id_user)):
            return int(user[str(id_guild)])
        return 0

    def set_user_points_db(self, id_user: int, id_guild: int, points: int) -> None:
        self.__redis.hset(
            str(id_user),
            mapping={id_guild: points}
        )
