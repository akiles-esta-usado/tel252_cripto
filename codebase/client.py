import asyncio
from aiohttp import ClientSession

from Crypto.Cipher import AES
from Crypto.PublicKey import ECC
from Crypto.Random import get_random_bytes

from base64 import b64decode, b64encode

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


async def to_server(file):
    global keys
    global ID0

    async with ClientSession() as session:

        # Generar el mensaje
        with open(file, "rb") as f:
            msg = f.read()

        id = ID0.to_bytes(1, "big")

        print(f"Se envia el mensaje: {str(msg)}")

        # Setear el cifrador
        cipher = AES.new(keys["session"], mode=AES.MODE_GCM)
        cipher.update(id)

        ct, tag = cipher.encrypt_and_digest(msg)

        result = {
            "nonce":      b64encode(cipher.nonce).decode('utf-8'),
            "header":     b64encode(id).decode('utf-8'),
            "ciphertext": b64encode(ct).decode('utf-8'),
            "tag":        b64encode(tag).decode('utf-8')
        }

        # Enviar el mensaje
        res = await session.post(URL + "data", json=result)
        data = await res.json()

        # Verificar el mensaje
        if (data["status"] == "NOK"):
            print("Los datos no se transmitieron correctamente")
            exit(-1)

        # Actualizar llave de sesión
        updateSessionKey()


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
    global keys

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

        print(data)

        if (data["status"] == "NOK"):
            print("Nonce no fué aceptado")
            exit(-1)

        # generamos la primera llave de sesión
        updateSessionKey(nonce)

    # Comenzamos a enviar los datos
    await to_server("data/data1.txt")

    await to_server("data/data2.txt")

    await to_server("data/data3.txt")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
