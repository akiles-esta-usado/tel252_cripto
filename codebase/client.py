import asyncio
from aiohttp import ClientSession

from Crypto.Cipher import AES
from Crypto.PublicKey import ECC
from Crypto.Random import get_random_bytes

from certificate_operations import obtainCertificate, verifyCertificate

from globals import URL

# from certificate_operations import gen_cert, ver_cert

keys = {
    "CA_pub": None,
    "priv": None,
    "pub": None,
    "secret_shared": None,
    "master": None,
    "session": None
}

ID0 = 10


def setKeys():
    global keys

    with open("keys/ca_pub_key_ECC.pem", "r") as f:
        keys["CA_pub"] = ECC.import_key(f.read())

    keys["priv"] = ECC.generate(curve="p256")
    keys["pub"] = keys["priv"].public_key()
    keys['session'] = int.from_bytes(get_random_bytes(16), "big")  # NONCE

    # guardar en algún archivo.


async def main():
    global ID0

    setKeys()

    async with ClientSession() as session:

        # Generar certificados de mis llaves
        my_cert = await obtainCertificate(session, ID0, keys["priv"], keys["pub"], keys["CA_pub"])

        if (my_cert == None):
            print("El certificado no se pudo obtener")
            exit(-1)

        # Intercambio de certificados con servidor
        res = await session.post(URL + "gen_shared_key", json=my_cert)
        server_cert = await res.json()

        # Verificar certificado del servidor
        if(verifyCertificate(server_cert, keys["CA_pub"]) == False):
            print("El certificado del servidor no es válido")
            exit(-1)

        # Generar la llave secreta compartida y la llave maestra
        k_pub_server = ECC.import_key(server_cert["k_pub"])

        keys["secret_shared"] = keys["priv"].d * k_pub_server.pointQ
        keys['master'] = keys["secret_shared"].x.to_bytes()[0:16]

        print(f'llave secreta compartida (x) :{keys["secret_shared"].x}')
        print(f'llave maestra :{keys["master"]}')

        # keys['session'] = updateSessionKey(keys['master'], keys['session'])
        # print(f"Llaves de sesión: {int.from_bytes(keys['session'],'big')}")

        return

        # Generar la llave de sesión

        return

        print(f"Certificado de servidor: {server_cert}")

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
