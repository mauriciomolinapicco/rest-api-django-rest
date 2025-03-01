import requests

endpoint = "http://localhost:8000/api/products/5/delete/"

res = requests.delete(endpoint)

if res.text:
    print(res.json())
else:
    print("Respuesta vacía:", res.status_code)