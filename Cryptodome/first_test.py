from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC)
decipher = AES.new(key, AES.MODE_CBC)

# Encrypt
pt = b"test"
ct_bytes = cipher.encrypt(pad(pt, AES.block_size))

ct = b64encode(ct_bytes).decode("utf-8")

print("pt: ", pt)
print("ct: ", ct)

# Decrypt
ct_bytes = b64decode(ct)

pt = unpad(decipher.decrypt(ct_bytes), AES.block_size)
print("pt: ", pt)
