import aioredis
import redis


async def PostConnectionKeys(id, keys):
    conn = redis.StrictRedis(host="localhost")
    conn.set(f"sensor{id}", keys)


async def getConnectionKeys(id):
    keys = {
        "server_priv": None,
        "server_pub": None,
        "shared_secret": None,
        "shared_master": None,
        "shared_session": None
    }
    conn = await aioredis.create_connection('redis://localhost')

    conn.execute("GET", "sensor"+id)
