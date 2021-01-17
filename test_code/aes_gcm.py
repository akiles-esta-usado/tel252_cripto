from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

# Encriptar
header = b"header"
data = b"hola amigos"

key = get_random_bytes(16)

cipher = AES.new(key, AES.MODE_GCM)

cipher.update(header)

(ciphertext, tag) = cipher.encrypt_and_digest(data)

result = {
    "nonce":      b64encode(cipher.nonce).decode('utf-8'),
    "header":     b64encode(header).decode('utf-8'),
    "ciphertext": b64encode(ciphertext).decode('utf-8'),
    "tag":        b64encode(tag).decode('utf-8')
}

print("encriptado: ", result)

# Desencriptar
json_input = result

try:
    b64 = json_input

    jv = {
        'nonce':      b64decode(b64['nonce']),
        'header':     b64decode(b64['header']),
        'ciphertext': b64decode(b64['ciphertext']),
        'tag':        b64decode(b64['tag'])
    }

    cipher = AES.new(key, AES.MODE_GCM, nonce=jv['nonce'])

    cipher.update(jv['header'])
    plaintext = cipher.decrypt_and_verify(
        jv['ciphertext'],
        jv['tag']
    )

    print("The message was: " + str(plaintext))

except [ValueError, KeyError]:
    print("Incorrect decryption")
