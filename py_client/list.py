import requests

endpoint = "http://localhost:8000/api/products/"

data = {"title":"new", "price":100.99}
res = requests.get(endpoint, json=data)

print(res.json())