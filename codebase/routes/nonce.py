from aiohttp import web

from globals import getCAPubKey, getConnectionKeys, postConnectionKeys, showKeys, updateSessionKey
from certificate_operations import verifyNonce

nonce_router = web.RouteTableDef()

# ----->NO ENTRA A ESTE ARCHIVO EL CODIGO


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

# -------->SUPOSICION-> TALVEZ HAY PROBLEMA AL PEDIR LAS KEYS, DEBIDO A LOS CONDICIONALES QUE HAY EN LA FUNCION
    # getConnectionKeys()

    keys = getConnectionKeys(sensor_id)

    CA_pub = getCAPubKey()

    # Verificamos la firma del sensor.
    if(verifyNonce(data, keys["sensor_pub"]) == False):
        print("El certificado no es válido")
        return web.json_response({"status": "NOK"})

    # Creamos la llave de sesión
    updateSessionKey(sensor_id, data["nonce"])

    return web.json_response({
        "status": "OK"
    })

    # depuración
    print("nonce.nonce_handler:")
    showKeys()
