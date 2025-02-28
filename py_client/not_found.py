import requests

endpoint = "http://localhost:8000/api/products/178989789897897897789799789"

res = requests.get(endpoint, json={})

print(res.text)