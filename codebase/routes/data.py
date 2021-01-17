from aiohttp import web

from Crypto.Cipher import AES

from base64 import b64decode

from globals import URL, getSessionKey, updateSessionKey

data_router = web.RouteTableDef()


@data_router.post("/data")
async def data_post_handler(request):
    temp_data = await request.json()

    # Decodificamos a bytes los datos que llegaron.
    jv = {
        'nonce':      b64decode(temp_data['nonce']),
        'header':     b64decode(temp_data['header']),
        'ciphertext': b64decode(temp_data['ciphertext']),
        'tag':        b64decode(temp_data['tag'])
    }

    # Obtenemos la llave de sesión
    id = int.from_bytes(jv["header"], "big")
    key = getSessionKey(id)

    try:

        cipher = AES.new(key,
                         AES.MODE_GCM,
                         nonce=jv['nonce']
                         )

        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(
            jv['ciphertext'],
            jv['tag']
        )

        print("The message was: " + str(plaintext))

        updateSessionKey(id)

        return web.json_response({
            "status": "OK"
        })

    except:
        print("Incorrect decryption")

        return web.json_response({
            "status": "NOK"
        })
