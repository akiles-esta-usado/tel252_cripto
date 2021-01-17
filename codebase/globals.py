from Crypto.Cipher import AES
from Crypto.PublicKey import ECC

#URL = "http://40.87.109.190:8080/"
URL = "http://localhost:8080/"

key_db = {}

CA_keys = {}

# CA Key Operations


def setCAKeys():
    with open("keys/ca_priv_key_ECC.pem", "rb") as f:
        CA_keys["priv"] = ECC.import_key(f.read())

    with open("keys/ca_pub_key_ECC.pem", "rb") as f:
        CA_keys["pub"] = ECC.import_key(f.read())


def getCAPubKey():
    return CA_keys["pub"]


def getCAPrivKey():
    return CA_keys["priv"]


# DataBase Operations
def postConnectionKeys(id, keys):
    global key_db
    label = f"sensor{id}"
    key_db[label] = keys


def getConnectionKeys(id=-1):
    global key_db

    if (id == -1 or f"sensor{id}" not in key_db):
        return {
            "server_priv": None,
            "server_pub": None,
            "sensor_pub": None,
            "shared_secret": None,
            "shared_master": None,
            "shared_session": None
        }
    return key_db[f"sensor{id}"]


def updateSessionKey(id, nonce=-1):
    global key_db
    label = f"sensor{id}"

    if(label not in key_db):
        return None

    keys = key_db[label]

    if (nonce == -1):
        last_session = keys["shared_session"]

    else:
        last_session = nonce.to_bytes(16, "big")

    cipher = AES.new(keys["shared_master"], mode=AES.MODE_ECB)
    keys["shared_session"] = cipher.encrypt(last_session)

    postConnectionKeys(id, keys)


def setKeys(id):
    global key_db

    keys = getConnectionKeys(id)

    keys["server_priv"] = ECC.generate(curve="p256")
    keys["server_pub"] = keys["server_priv"].public_key()

    postConnectionKeys(id, keys)

    return keys


def showKeys():
    global CA_keys
    global key_db

    for label in CA_keys.keys():
        print(f"{label}: {type(CA_keys[label])}")
        print(f"{CA_keys[label]}")
        print("")

    for label in key_db.keys():
        print(f"{label}:")

        for key_name in key_db[label].keys():
            print(f"  {key_name}: {type(key_db[label][key_name])}")
            print(f"  {key_db[label][key_name]}")
            print("")
