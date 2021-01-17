from Crypto.Hash import SHA256
from Crypto.Signature import DSS

import base64
import json

from globals import URL


def generateSign(msg, k_priv):
    """
    msg: es un diccionario
    k_priv: llave pública instancia de EccKey

    Esta función retorna una tupla:
    sign <str>: La firma en base 64.
    hash_digest <SHA256Hash>: Objeto hash del mensaje.
    """

    hash = SHA256.new(
        json.dumps(msg).encode('utf-8')
    )

    signer = DSS.new(k_priv, 'fips-186-3')
    msg_sign = signer.sign(hash)

    return (base64.urlsafe_b64encode(msg_sign).decode("utf-8"))


def verifyNonce(cert, k_pub):
    """
    cert: {
        id: string, number
        k_pub: 
        sign: bytes
    }
    """
    message = {
        "id": cert["id"],
        "nonce": cert["nonce"]
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


async def obtainCertificate(session, id, k_priv, k_pub, ca_k_pub, nonce=-1):
    """
    Las llaves deben ingresar como objetos EccKey
    El certificado se retorna con formatos PEM, base64.
    """
    message = None

    if (nonce == -1):
        message = {
            "id": id,
            "k_pub": k_pub.export_key(format="PEM")
        }
    else:
        message = {
            "id": id,
            "k_pub": k_pub.export_key(format="PEM"),
            "k_session": nonce
        }

    hash_digest = SHA256.new(
        json.dumps(message).encode('utf-8')
    )

    signer = DSS.new(k_priv, 'fips-186-3')
    message_sign = signer.sign(hash_digest)

    message["sign"] = base64.urlsafe_b64encode(message_sign).decode("utf-8")

    resp = await session.post(URL + "get_cert", json=message)
    cert = await resp.json()

    cert_sign = base64.urlsafe_b64decode(cert["sign"])
    verifier = DSS.new(ca_k_pub, 'fips-186-3')

    try:
        verifier.verify(hash_digest, cert_sign)
        return cert

    except ValueError:
        return None
