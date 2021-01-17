from aiohttp import web
import redis
import aioredis
import json

nonce_router = web.RouteTableDef()

@nonce_router.post("/set_Nonce")

async def nonce_code(request):
     conn = await aioredis.create_connection('redis://localhost')
     nonce = await request.json()

    print("El nonce es: ", nonce)