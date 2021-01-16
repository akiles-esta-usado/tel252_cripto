from Crypto.Cipher import AES

from constants import URL


def updateSessionKey(k_master, prev):
    cipher = AES.new(k_master, mode=AES.MODE_ECB)
    next = cipher.encrypt(prev)

    return next
