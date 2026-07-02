import asyncio
import json

import redis.asyncio as redis

REDIS_HOST = "192.168.197.128"
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
    password= "********"

)
async def init_redis_test():
    try:
        res = await redis_client.ping()
        if res:
            print("✅ Redis 连接成功")
        # 关键：前面加 await
        await redis_client.setex("news:categories", 3600, 3)
        val = await redis_client.get("news:categories")
        print(f"存入后读取值：{val}")
    except Exception as e:
        print("❌ 连接失败:", e)
async def get_cache(key):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"Error getting cache: {e}")
        return None

async def get_json_cache(key):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"Error getting JSON cache: {e}")
        return None

async def set_cache(key, value, expire=3600):
    try:
        is_instance = isinstance(value, (dict, list))
        if is_instance:
            value = json.dumps(value,ensure_ascii=False)
        await redis_client.setex(key, expire,value)
        return True
    except Exception as e:
        print(f"Error setting cache: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(init_redis_test())