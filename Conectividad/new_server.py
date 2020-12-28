from aiohttp import web

from routes.test import test_route

app = web.Application()

app.add_routes(test_route)

if __name__ == "__main__":
    web.run_app(app)
