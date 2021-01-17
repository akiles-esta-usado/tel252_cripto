from aiohttp import web
from globals import getCAPrivKey

from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import base64
import json

cert_router = web.RouteTableDef()


@cert_router.post("/get_cert")
async def cert_handle_get(request):

    data = await request.json()

    ca_k_pr = getCAPrivKey()

    id = data["id"]
    k_pub = data["k_pub"]

    sign = base64.urlsafe_b64decode(data["sign"])

    # Verificar la firma con mi llave privada
    message = {
        "id": id,
        "k_pub": k_pub
    }

    bytes_message = json.dumps(message).encode('utf-8')

    h = SHA256.new(bytes_message)
    verifier = DSS.new(ECC.import_key(data["k_pub"]), 'fips-186-3')

    try:
        verifier.verify(h, sign)
        print("The message is authentic.")

    except ValueError:
        print("The message is not authentic.")
        return web.json_response(json={"status": "NOK", "desc": "firma no coincide"})

    # Generar el certificado, que es una firma con mi llave privada
    signer = DSS.new(ca_k_pr, 'fips-186-3')
    sign = signer.sign(h)

    cert = {
        "id": id,
        "k_pub": k_pub,
        "sign": base64.urlsafe_b64encode(sign).decode("utf-8")
    }

    return web.json_response(cert)
