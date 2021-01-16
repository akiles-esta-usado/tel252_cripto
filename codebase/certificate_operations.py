import asyncio
from aiohttp import ClientSession

from Crypto.PublicKey import ECC
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

import base64
import json


def verifyCertificate(cert, k_pub):
    """
    cert: {
        id: string, number
        k_pub: str PEM
        sign: bytes
    }
    """
    message = {
        "id": cert.id,
        "k_pub": cert.k_pub
    }

    bytes_message = json.dumps(message).encode('utf-8')
    h = SHA256.new(bytes_message)

    sign = base64.urlsafe_b64decode(cert["sign"])

    verifier = DSS.new(k_pub, 'fips-186-3')

    try:
        verifier.verify(h, sign)
        print("El certificado es auténtico.")

        return True

    except ValueError:
        print("El certificado no es auténtico.")
        return False


async def obtainCertificate(session, id, k_priv, k_pub, ca_k_pub):
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

    from_CA = await session.post("http://localhost:8080/get_cert", json=to_CA)

    data = await from_CA.json()

    sign = base64.urlsafe_b64decode(data["sign"])

    verifier = DSS.new(ca_k_pub, 'fips-186-3')

    try:
        verifier.verify(h, sign)
        print("El certificado es auténtico.")

        return {
            "id": id,
            "k_pub": k_pub,
            "sign": sign
        }

    except ValueError:
        print("El certificado no es auténtico.")
        return None
