from aiohttp import web

from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import base64
import json

import aioredis

from certificate_operations import obtainCertificate, verifyCertificate

url = "http://localhost:8080/"

exchange_router = web.RouteTableDef()


@exchange_router.post("/gen_shared_key")
async def shared_key_handler(request):
    sensor_cert = await request.json()

    conn = await aioredis.create_connection(
        'redis://localhost')

    ca_k_pr = ECC.import_key(
        await conn.execute('GET', 'ca_priv_key', encoding="utf-8")
    )

    ca_k_pub = ECC.import_key(
        await conn.execute('GET', 'ca_pub_key', encoding="utf-8")
    )

    print(sensor_cert)

    return web.json_response({"error": "Hola"})
