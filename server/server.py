import sys

from aiohttp import web

import aioredis

from aiohttp_session import setup
from aiohttp_session.redis_storage import RedisStorage

from routes.index import index_router


async def make_app():
    app = web.Application()
    redis = None

    try:
        redis = await aioredis.create_pool(('localhost', 6379))

        setup(app, RedisStorage(redis))

        app.add_routes(index_router)

        return app

    except ConnectionRefusedError as e:
        print(f"Error de conexión: rechazada (¿Servidor redis esta inicializado?)")
        sys.exit(-1)

    except Exception as e:
        print(f"Error:  {e}")
        sys.exit(-1)


if __name__ == "__main__":
    try:
        web.run_app(make_app())

    except Exception as e:
        print(f"Error: Aplicación falló")
        sys.exit(-1)
