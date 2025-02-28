import requests

endpoint = "http://localhost:8000/api"

res = requests.get(endpoint, params={"abc":123}, json={"product_id":1234})

print(res.text)
print(res.status_code)