import requests
from getpass import getpass

auth_endpoint = "http://localhost:8000/api/auth/"
password = getpass("Enter password: ")
auth_response = requests.post(auth_endpoint, json={"username":"staff", "password":password})
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    endpoint = "http://localhost:8000/api/products/"
    res = requests.get(endpoint, headers=headers)
    print(res.json())