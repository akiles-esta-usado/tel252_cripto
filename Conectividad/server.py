from socketserver import BaseRequestHandler, TCPServer


class Servidor:

    def __init__(self, port):
        if (type(port) != int):
            raise TypeError("el puerto debe ser un entero")

        self.server = TCPServer(('', port), self.Handler)

        print('Servidor TCP iniciado en puerto {0}'.format(port))

        self.server.serve_forever()

    class Handler(BaseRequestHandler):
        def handle(self):
            print('Se ha conectado {0}'.format(self.client_address))

            while True:
                msj = self.request.recv(8192)

                if not msj:
                    break
                self.request.send(msj)


if __name__ == '__main__':

    port = 20664
    Servidor(port)
