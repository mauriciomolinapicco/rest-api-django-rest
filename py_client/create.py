import requests

endpoint = "http://localhost:8000/api/products/"

data = {"title":"CREado con mixins", "price":100.99}
res = requests.post(endpoint, json=data)

print(res.json()) 