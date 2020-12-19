from Conectividad.client import Cliente

addr = "localhost"
port = 20664

cliente = Cliente(addr, port)

valor = 10000000
cliente.send(valor)

respuesta = cliente.recv()

print(respuesta)
