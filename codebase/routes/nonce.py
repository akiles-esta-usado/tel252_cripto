from aiohttp import web

from globals import getCAPubKey, getConnectionKeys, postConnectionKeys, showKeys, updateSessionKey
from certificate_operations import verifyCertificate

nonce_router = web.RouteTableDef()


@nonce_router.post("/set_Nonce")
async def nonce_code(request):
    """
    request: {
        id: ...
        nonce: ...
        sign: hecha por el sensor
    }
    """

    data = await request.json()
    sensor_id = data["id"]

    keys = getConnectionKeys(sensor_id)

    CA_pub = getCAPubKey()

    # Verificamos la firma del sensor.
    if(verifyCertificate(data, keys["sensor_pub"]) == False):
        print("El certificado no es válido")
        return web.json_response({"status": "NOK"})

    # Creamos la llave de sesión
    nonce = int.from_bytes(data["nonce"], "big")
    updateSessionKey(sensor_id, nonce)

    # depuración
    showKeys()
    print('Llave mosttradas')
