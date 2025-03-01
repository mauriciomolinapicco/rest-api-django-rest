import requests

endpoint = "http://localhost:8000/api/products/1/update/"

data = {"title":"Updatedd", "price":129.99}

res = requests.put(endpoint, json=data)

print(res.text)