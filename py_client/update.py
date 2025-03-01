import requests

endpoint = "http://localhost:8000/api/products/1/update/"

data = {"title":"Hello old friend", "price":129.99}

res = requests.put(endpoint, json=data)

print(res.text)