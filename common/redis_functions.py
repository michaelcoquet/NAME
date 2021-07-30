import redis
import json
from django.conf import settings

redis_db = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def set(id, data):
    data = json.dumps(data)
    redis_db.set("top_tracks:" + id, data)


def get(id):
    data = redis_db.get(id)
    return data
