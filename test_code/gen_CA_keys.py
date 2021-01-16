from Crypto.PublicKey import ECC

k_priv = ECC.generate(curve="p256")
k_pub = k_priv.public_key()


k_priv_PEM = k_priv.export_key(format="PEM")
k_pub_PEM = k_pub.export_key(format="PEM")

with open("ca_priv_key_ECC.pem", "w") as file_out:
    file_out.write(k_priv_PEM)
    file_out.close()


with open("ca_pub_key_ECC.pem", "w") as file_out:
    file_out.write(k_pub_PEM)
    file_out.close()
