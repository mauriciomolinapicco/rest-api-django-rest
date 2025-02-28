import requests

endpoint = "http://localhost:8000/api/"

res = requests.post(endpoint, json={"title":None})

print(res.text)
# print(res.headers)