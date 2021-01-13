from aiohttp import web
from aiohttp_session import get_session, setup, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import asyncio

from cryptography import fernet
from base64 import urlsafe_b64decode

test_route = web.RouteTableDef()


@test_route.post("/data/")
async def test_post_data(request):
    post_data = await request.post()

    print("largo de post: ", len(post_data))

    for i in post_data.items():
        print(i)

    return web.json_response({
        "largo": len(post_data)
    })


@test_route.get("/session/")
async def test_session(request):
    session = await get_session(request)

    last_visit = session['last_visit'] if 'last_visit' in session else None

    return web.json_response({
        "last_visited": last_visit
    })


async def make_app():

    app = web.Application()

    key = fernet.Fernet.generate_key()
    key_urlsafe = urlsafe_b64decode(key)

    setup(app, EncryptedCookieStorage(key_urlsafe))

    app.add_routes(test_route)
    return app

if __name__ == "__main__":
    web.run_app(make_app())
