from globals import setCAKeys
from aiohttp import web
from routes.index import index_router
from routes.certificates import cert_router
from routes.key_exchange import exchange_router
from routes.nonce import nonce_router
from routes.data import data_router


async def make_app():
    app = web.Application()
    setCAKeys()
    app.add_routes(index_router)
    app.add_routes(cert_router)
    app.add_routes(exchange_router)
    app.add_routes(nonce_router)
    app.add_routes(data_router)

    return app


if __name__ == "__main__":
    try:
        web.run_app(make_app())

    except Exception as e:
        print(f"Error: Aplicación falló")
        exit(-1)
