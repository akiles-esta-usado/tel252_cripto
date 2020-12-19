from socketserver import BaseRequestHandler, TCPServer


class Servidor:

    def __init__(self):
        self.server = TCPServer(('', 20664), self.Handler)
        print('Servidor TCP iniciado')
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
    Servidor()
