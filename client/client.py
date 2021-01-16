import asyncio
from aiohttp import ClientSession

from Crypto.PublicKey import ECC
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

import base64
import json

# from certificate_operations import gen_cert, ver_cert

keys = {
    "CA_pub": None,
    "priv": None,
    "pub": None
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


async def obtainCertificate(id, k_priv, k_pub, ca_k_pub):
    # Generación del mensaje
    message = {
        "id": id,
        "k_pub": k_pub.export_key(format="PEM")
    }

    bytes_message = json.dumps(message).encode('utf-8')
    h = SHA256.new(bytes_message)

    signer = DSS.new(k_priv, 'fips-186-3')
    sign = signer.sign(h)

    to_CA = {
        "id": id,
        "k_pub": k_pub.export_key(format="PEM"),
        "sign": base64.urlsafe_b64encode(sign).decode("utf-8")
    }

    async with ClientSession() as session:

        from_CA = await session.post(url + "get_cert", json=to_CA)

        data = await from_CA.json()

        sign = base64.urlsafe_b64decode(data["sign"])

        verifier = DSS.new(ca_k_pub, 'fips-186-3')

        try:
            verifier.verify(h, sign)
            print("El certificado es auténtico.")

            return sign

        except ValueError:
            print("El certificado no es auténtico.")
            return None


async def main():
    global ID0
    global url

    setKeys()

    sign = await obtainCertificate(ID0, keys["priv"], keys["pub"], keys["CA_pub"])

    print(sign)

    return

    async with ClientSession() as session:
        await gets(session)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
