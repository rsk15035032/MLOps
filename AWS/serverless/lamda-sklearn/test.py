import requests
import json

URL = "http://localhost:8080/2015-03-31/functions/function/invocations"

with open("customer.json", "r") as f:
    data = json.load(f)

response = requests.post(URL, json=data)

print("Status:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))