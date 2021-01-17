from aiohttp import web, ClientSession

from Crypto.PublicKey import ECC

from certificate_operations import obtainCertificate, verifyCertificate

from globals import URL, getCAPubKey, getConnectionKeys, postConnectionKeys, setKeys, showKeys

exchange_router = web.RouteTableDef()


@exchange_router.post("/gen_shared_key")
async def shared_key_handler(request):
    sensor_cert = await request.json()

    CA_pub = getCAPubKey()

    # Verificamos el certificado del sensor.
    if(verifyCertificate(sensor_cert, CA_pub) == False):
        print("El certificado no es válido")
        return web.json_response({"status": "NOK"})

    sensor_id = sensor_cert["id"]
    keys = setKeys(sensor_id)

    # Generamos un certificado para las llaves.
    async with ClientSession() as session:
        my_cert = await obtainCertificate(session, 0, keys["server_priv"], keys["server_pub"], CA_pub)

        if (my_cert == None):
            print("El certificado no se pudo obtener")
            return web.json_response({"status": "NOK"})

    # Verificamos nuestro certificado
    if(verifyCertificate(my_cert, CA_pub) == False):
        print("El certificado no es válido")
        return web.json_response({"status": "NOK"})

    # Generamos llave secreta de sesión
    keys["sensor_pub"] = ECC.import_key(sensor_cert["k_pub"])
    keys['shared_secret'] = keys["server_priv"].d * keys["sensor_pub"].pointQ
    keys["shared_master"] = keys['shared_secret'].x.to_bytes()[0:16]

    postConnectionKeys(sensor_id, keys)

    # showKeys()

    return web.json_response(my_cert)
