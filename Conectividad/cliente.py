from socket import socket, AF_INET, SOCK_STREAM

s = socket(AF_INET,SOCK_STREAM)
s.connect(('localhost',20664))
s.send(b'Hola desde cliente local')
s.recv(8192)
