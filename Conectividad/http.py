from urllib import parse, request
import requests
import math


# url = 'http://httpbin.org/post'
# data = {
#     'lenguaje': 'Python',
#     'version':'3.8.5',
#     'Key-public': 'A'
# }

# res = requests.post(url,data=data ,stream=True)
# texto_claro = res.text
# print(texto_claro)
class Cliente:
    def __init__(self,generator,modulo):
        self.generator = generator
        self.modulo = modulo

    def __set_generator(self,generator):
        if (math.gcd(generator,modulo) == 1):
            self.generator = generator
        else:
            print('No se pudo instanciar el generador')

    def metodo_prueba(self):
        return generator * modulo