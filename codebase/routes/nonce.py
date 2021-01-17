from aiohttp import web

from globals import getCAPubKey, getConnectionKeys, postConnectionKeys, showKeys, updateSessionKey
from certificate_operations import verifyCertificate

nonce_router = web.RouteTableDef()

##----->NO ENTRA A ESTE ARCHIVO EL CODIGO
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

##-------->SUPOSICION-> TALVEZ HAY PROBLEMA AL PEDIR LAS KEYS, DEBIDO A LOS CONDICIONALES QUE HAY EN LA FUNCION
    ##              getConnectionKeys()


    keys = getConnectionKeys(sensor_id)

    CA_pub = getCAPubKey()

    # Verificamos la firma del sensor.
    if(verifyCertificate(data, keys["sensor_pub"]) == False):
        print("El certificado no es válido")
        return web.json_response({"status": "NOK"})

    # Creamos la llave de sesión
    nonce = int.from_bytes(data["nonce"], "big")
    updateSessionKey(sensor_id, nonce)


##------>PROBLEMA, NO MUESTRA LAS KEYS


    # depuración
    showKeys()
    print('Llave mosttradas')
