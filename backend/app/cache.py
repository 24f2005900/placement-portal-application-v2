import json
import redis

# connect to local redis. if redis isn't running the app still works,
# we just skip the cache (see the try/except in each function below)
client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
    socket_connect_timeout=1,
)


def get_cache(key):
    try:
        value = client.get(key)
        return json.loads(value) if value else None
    except Exception:
        return None


def set_cache(key, value, ttl=60):
    try:
        client.set(key, json.dumps(value), ex=ttl)
    except Exception:
        pass


def clear_cache(key):
    try:
        client.delete(key)
    except Exception:
        pass
