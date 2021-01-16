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
        k_pub: 
        sign: bytes
    }
    """
    message = {
        "id": cert["id"],
        "k_pub": cert["k_pub"]
    }

    bytes_message = json.dumps(message).encode('utf-8')
    h = SHA256.new(bytes_message)

    sign = base64.urlsafe_b64decode(cert["sign"])

    verifier = DSS.new(k_pub, 'fips-186-3')

    try:
        verifier.verify(h, sign)
        return True

    except ValueError:
        return False


async def obtainCertificate(session, id, k_priv, k_pub, ca_k_pub):
    """
    Las llaves deben ingresar como objetos EccKey
    El certificado se retorna con formatos PEM, base64.
    """

    message = {
        "id": id,
        "k_pub": k_pub.export_key(format="PEM")
    }

    hash_digest = SHA256.new(
        json.dumps(message).encode('utf-8')
    )

    signer = DSS.new(k_priv, 'fips-186-3')
    message_sign = signer.sign(hash_digest)

    message["sign"] = base64.urlsafe_b64encode(message_sign).decode("utf-8")

    resp = await session.post("http://localhost:8080/get_cert", json=message)
    cert = await resp.json()

    cert_sign = base64.urlsafe_b64decode(cert["sign"])
    verifier = DSS.new(ca_k_pub, 'fips-186-3')

    try:
        verifier.verify(hash_digest, cert_sign)
        return cert

    except ValueError:
        return None
