from multiprocessing.connection import Listener
import traceback

def cliente (conexion):
    try:
        while True:
            msj = conexion.recv()
            conexion.send(msj)
    except EOFError:
        print('Conexion errronea')

def servidor(direccion, clave):
    s = Listener(direccion,clave)

    while True:
        try:
            c = s.accept()
            cliente(c)
        except Exception:
            traceback.print_exc()


servidor(('192.168.0.6',20064),b'estaserialaclave')

