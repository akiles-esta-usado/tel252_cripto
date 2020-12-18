from urllib import parse, request
import requests


url = 'http://httpbin.org/post'
data = {
    'lenguaje': 'Python',
    'version':'3.8.5',
    'Key-public': 'A'
}

res = requests.post(url,data)
texto_claro = res.text
print(texto_claro)

