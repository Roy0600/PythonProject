import requests
import json
from random import randrange

count = 0

while count <= 50:
    # Random name api
    url = "https://namey.muffinlabs.com/name.json?with_surname=true"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text.replace("[\"", "").replace("\"]", ""))

    name = response.text.replace("[\"", "").replace("\"]", "")

    url = "http://127.0.0.1:5000/api/v1/user"

    payload = json.dumps({
        "name": name,
        # Random number between 0 and 100
        "score": str(randrange(100))
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    count += 1
