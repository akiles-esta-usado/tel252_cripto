from globals import showKeys, setCAKeys
import sys
from aiohttp import web
import redis
from routes.index import index_router
from routes.certificates import cert_router
from routes.key_exchange import exchange_router


def setKeys():
    redis_conn = redis.StrictRedis(host="localhost")

    with open("keys/ca_priv_key_ECC.pem", "rb") as f:
        redis_conn.set(b"ca_priv_key", f.read())

    with open("keys/ca_pub_key_ECC.pem", "rb") as f:
        redis_conn.set(b"ca_pub_key", f.read())


async def make_app():
    app = web.Application()

    # setKeys()
    setCAKeys()
    showKeys()

    app.add_routes(index_router)
    app.add_routes(cert_router)
    app.add_routes(exchange_router)

    return app


if __name__ == "__main__":
    try:
        web.run_app(make_app())

    except Exception as e:
        print(f"Error: Aplicación falló")
        sys.exit(-1)
