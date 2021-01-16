from aiohttp import web

from aiohttp_session import get_session

index_router = web.RouteTableDef()


@index_router.get("/")
async def index_handle_get(request):

    print(f"request url: {request.url}")
    print(f"request cookie: {request.cookies}")
    print(f"request query: {request.query}")

    session = await get_session(request)

    if ("visited" in session):
        session['visited'] += 1
        visited = session['visited']

    else:
        visited = session['visited'] = 0

    return web.json_response({
        "times visited": visited
    })


@index_router.post("/")
async def index_handle_post(request):
    try:
        data = await request.json()

        return web.json_response({
            "status": "success",
            "message": f"creado el usuario {data['user']}"
        })

    except Exception as e:
        return web.json_response({
            "status": "failed",
            "error": e
        })
