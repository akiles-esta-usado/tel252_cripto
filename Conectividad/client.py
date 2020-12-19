from socket import socket, AF_INET, SOCK_STREAM


class Cliente:
    def __init__(self, addr, port):
        if(type(addr) != str):
            raise TypeError("Dirección debe ser string")

        if(type(port) != int):
            raise TypeError("Puerto debe ser entero")

        self.socket = socket(AF_INET, SOCK_STREAM)

        try:
            self.socket.connect((addr, port))
        except:
            print("Error de conexión")

    def send(self, valor, length=10):
        """
        Asume que trabajamos con valores enteros
        """

        if (type(valor) != int):
            raise TypeError("Solo se envian enteros")

        valor_bytes = valor.to_bytes(length, "big")
        self.last_len = self.socket.send(valor_bytes)

    def recv(self):
        message_bytes = self.socket.recv(self.last_len)

        message = int.from_bytes(message_bytes, "big")

        return message


if __name__ == "__main__":
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 20664))
    # len = s.send(b'Hola desde cliente local')
    # len = s.send(int.to_bytes(10000000000000))

    numero = 2**10
    numero_bytes = numero.to_bytes(10, "big")
    print(numero_bytes)
    len = s.send(numero_bytes)

    print("Enviado mensaje de {0} bits".format(len))
    print(int.from_bytes(s.recv(len), "big"))
