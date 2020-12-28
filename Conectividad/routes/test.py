from aiohttp import web
from aiohttp import web

test_route = web.RouteTableDef()


@test_route.get("/test/")
@test_route.get("/test/{name}")
async def test_handle(request):

    name = request.match_info.get("name", "Anonymous")

    text = "Hello " + name

    return web.Response(text=text)
