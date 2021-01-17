from aiohttp import web, ClientSession

from Crypto.PublicKey import ECC
import aioredis

from certificate_operations import obtainCertificate, verifyCertificate

from globals import URL, getCAPubKey, getConnectionKeys, postConnectionKeys

exchange_router = web.RouteTableDef()


@exchange_router.post("/gen_shared_key")
async def shared_key_handler(request):
    keys = getConnectionKeys()
    CA_pub = getCAPubKey()

    sensor_cert = await request.json()

    # Verificamos autenticidad del certificado entregado.
    if(verifyCertificate(sensor_cert, CA_pub) == False):
        print("El certificado no es válido")
        return web.json_response({"status": "NOK"})

    # Generamos un par de llaves.
    keys["server_priv"] = ECC.generate(curve="p256")
    keys["server_pub"] = keys["server_priv"].public_key()

    # Generamos un certificado para las llaves.
    async with ClientSession() as session:
        my_cert = await obtainCertificate(session, 0, keys["server_priv"], keys["server_pub"], CA_pub)

        if (my_cert == None):
            print("El certificado no se pudo obtener")
            return web.json_response({"status": "NOK"})

    # Verificamos el certificado
    if(verifyCertificate(my_cert, CA_pub) == False):
        print("El certificado no es válido")
        return web.json_response({"status": "NOK"})

    # Generamos llave secreta de sesión

    K_pub_sensor = ECC.import_key(sensor_cert["k_pub"])

    K_shared_secret = keys["server_priv"].d * K_pub_sensor.pointQ

    K_master = K_shared_secret.x.to_bytes()[0:16]

    print(f"llave secreta compartida (x) :{K_shared_secret.x}")
    print(f"llave maestra :{K_master}")

    return web.json_response(my_cert)
