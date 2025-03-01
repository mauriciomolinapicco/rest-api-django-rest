import requests

endpoint = "http://localhost:8000/api/products/11/delete/"

res = requests.delete(endpoint)

if res.text:
    print(res.json())
else:
    print("Eliminado correctamente:", res.status_code)