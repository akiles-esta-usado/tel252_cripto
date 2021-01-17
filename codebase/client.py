import asyncio
from aiohttp import ClientSession

from Crypto.Cipher import AES
from Crypto.PublicKey import ECC
from Crypto.Random import get_random_bytes

from certificate_operations import obtainCertificate, verifyCertificate, generateSign

from globals import URL

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


def showKeys(label=""):
    global keys

    if (label == ""):
        for key_name in keys.keys():
            print(f"  {key_name}: {type(keys[key_name])}")
            print(f"  {keys[key_name]}")
            print("")
        return

    print(f"  {label}: {type(keys[label])}")
    print(f"  {keys[label]}")
    print("")


def updateSessionKey(nonce=-1):
    global keys
    prev = None
    if (nonce == -1):
        prev = keys["session"]
        pass

    else:
        prev = nonce.to_bytes(16, "big")

    cipher = AES.new(keys["master"], mode=AES.MODE_ECB)
    keys["session"] = cipher.encrypt(prev)


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

        # Enviar el Nonce
        nonce = int.from_bytes(get_random_bytes(16), "big")  # NONCE

        message_nonce = {
            "id": ID0,
            "nonce": nonce
        }

        # Firmar Nonce con ID
        message_nonce["sign"] = generateSign(message_nonce, keys["priv"])

        # Enviamos nonce
        nonce_res = await session.post(URL + "set_Nonce", json=message_nonce)
        data = await nonce_res.json()

        if (data["status"] == "NOK"):
            print("Nonce no fué aceptado")
            exit(-1)

        # generamos la primera llave de sesión
        updateSessionKey(nonce)

        return


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
