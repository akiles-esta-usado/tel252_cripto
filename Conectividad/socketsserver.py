from socketserver import BaseRequestHandler, TCPServer

class Solicitudes(BaseRequestHandler):
    def handle(self):
        print('se ha concectado {}'.format(self.client_address))

        while True:
            msj = self.request.recv(8192)

            if not msj:
                break
            self.request.send(msj)


if __name__ == '__main__':
    server = TCPServer(('',20664),Solicitudes)
    print('Servidor TCP iniciado')
    server.serve_forever()


