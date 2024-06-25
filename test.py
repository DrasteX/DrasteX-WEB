import requests
import json

url = "https://sandbox.qikink.com/api/token"

payload = {
    "ClientId": "323252398360424",
    "client_secret": "5537d032b1ea68004b61e712ca5e89468633be92dbc0fc725be7d9061555ee51"
}
headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.text)
