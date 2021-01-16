from aiohttp import web, ClientSession

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
    keys = {
        "priv": None,
        "pub": None,
        "CA_pub": None
    }

    sensor_cert = await request.json()

    conn = await aioredis.create_connection('redis://localhost')

    keys["CA_pub"] = ECC.import_key(
        await conn.execute('GET', 'ca_pub_key', encoding="utf-8")
    )

    # Verificamos autenticidad del certificado entregado.
    if(verifyCertificate(sensor_cert, keys["CA_pub"]) == False):
        print("El certificado no es válido")
        return web.json_response({"status": "NOK"})

    # Generamos un par de llaves.
    keys["priv"] = ECC.generate(curve="p256")
    keys["pub"] = keys["priv"].public_key()

    # Generamos un certificado para las llaves.
    async with ClientSession() as session:
        my_cert = await obtainCertificate(session, 0, keys["priv"], keys["pub"], keys["CA_pub"])

        if (my_cert == None):
            print("El certificado no se pudo obtener")
            return web.json_response({"status": "NOK"})

    # Verificamos el certificado
    if(verifyCertificate(my_cert, keys["CA_pub"]) == False):
        print("El certificado no es válido")
        return web.json_response({"status": "NOK"})

    # Generamos llave secreta de sesión

    K_pub_sensor = ECC.import_key(sensor_cert["k_pub"])

    K_shared_secret = keys["priv"].d * K_pub_sensor.pointQ

    K_master = K_shared_secret.x.to_bytes()[0:15]

    print(f"llave secreta compartida (x) :{K_shared_secret.x}")
    print(f"llave maestra :{K_master}")

    return web.json_response(my_cert)
