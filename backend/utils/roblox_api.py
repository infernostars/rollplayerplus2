from random import randint

import requests


def get_random_roblox_username():
    response = requests.get(f"https://users.roblox.com/v1/users/{randint(1, 100_000_000)}")
    try:
        return response.json()["name"]
    except:
        print(response.text)
        return "too lazy to make an error handler, but lolfail"
