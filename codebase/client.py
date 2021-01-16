import asyncio
from aiohttp import ClientSession

from Crypto.PublicKey import ECC
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

import base64
import json

from certificate_operations import obtainCertificate, verifyCertificate

# from certificate_operations import gen_cert, ver_cert

keys = {
    "CA_pub": None,
    "priv": None,
    "pub": None,
    "secret_shared": None,
    "master_key": None,
    "session_key": None
}

ID0 = 10
url = "http://localhost:8080/"


def setKeys():
    global keys

    with open("keys/ca_pub_key_ECC.pem", "r") as f:
        keys["CA_pub"] = ECC.import_key(f.read())

    keys["priv"] = ECC.generate(curve="p256")
    keys["pub"] = keys["priv"].public_key()

    # guardar en algún archivo.


async def main():
    global ID0
    global url

    setKeys()

    async with ClientSession() as session:
        # Generar certificados de mis llaves
        my_cert = await obtainCertificate(session, ID0, keys["priv"], keys["pub"], keys["CA_pub"])

        if (my_cert == None):
            print("El certificado no se pudo obtener")
            exit(-1)

        print(my_cert)

        return

        # Enviar certificado a servidor, obtener certificado de servidor
        res = await session.post(url + "gen_shared_key/", json=my_cert)
        server_cert = await res.json()

        print(f"Certificado de servidor: {server_cert}")
        return

        if(verifyCertificate(server_cert, keys["CA_pub"]) == False):
            print("El certificado no es válido")
            exit(-1)

        # Generación de llaves secreta conjunta

        # Generación de llaves de sesión

    return

    async with ClientSession() as session:
        await gets(session)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
