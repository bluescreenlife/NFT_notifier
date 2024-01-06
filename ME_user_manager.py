import requests
import json

default_profile = {
    "user_no": 0,
    "available": "True",
    "email": "default@gmail.com",
    "urls": [
      "https://magiceden.io/ordinals/item-details/934224d8fa52b4a79ce1ee4596f6c6c3fb2966af89d314df162fd9ce3fa96597i0",
      "https://magiceden.io/ordinals/item-details/c7f83d24c9f868aecfa16d1efd12619430cf0fab7fdcc9bea3e5ae850b611303i0"
    ]
  }

def get_accounts():
    response = requests.get("https://api.npoint.io/4046dafca4a7c1e7753a")
    print(response.status_code)
    accounts = json.loads(response.text)
    return accounts

def post_accounts(data):
    data = json.dumps(data)
    response = requests.post("https://api.npoint.io/4046dafca4a7c1e7753a", data=data)
    print(response.status_code)

def add_user(email):
    accounts = get_accounts()
    new_user = {}
    new_user_index = 0

    for user in accounts:
        if user["available"] == "True":
            user["email"] = email
            user["available"] = "False"
            break

def remove_user(email):
    accounts = get_accounts()

    for user in accounts:
        if user["email"] == email:
            user = default_profile
            break

def add_url(email, url):
    accounts = get_accounts()

    for user in accounts:
        if user["email"] == email:
            user["urls"].append(url)
            break

def remove_url(email, url):
    accounts = get_accounts()

    for user in accounts:
        if user["email"] == email:
            user["urls"].remove(url)
            break