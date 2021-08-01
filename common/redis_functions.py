import redis
import json
from django.conf import settings

db = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def set(id, data):
    data = json.dumps(data)
    db.set(id, data)


def get(id):
    data = db.get(id)
    return data
