import redis.asyncio as redis
import json
from app.core.config import settings

redis_client: redis.Redis = None


async def connect_redis():
    global redis_client
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    print("Connected to Redis")


async def close_redis():
    if redis_client:
        await redis_client.close()


async def cache_set(key: str, value: dict, expire: int = 300):
    await redis_client.setex(key, expire, json.dumps(value, default=str))


async def cache_get(key: str):
    data = await redis_client.get(key)
    return json.loads(data) if data else None


async def cache_delete(key: str):
    await redis_client.delete(key)
