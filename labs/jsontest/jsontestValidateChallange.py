#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

import requests
import json
from pprint import pprint

URL = "http://validate.jsontest.com/"

def post_data(data: dict[str,any]) -> dict[str,any]:
    with open('data.json', 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)
    with open('data.json') as jsonfile:
        return requests.post(URL, jsonfile).json()

def get_datetime() -> str:
    return requests.get("http://date.jsontest.com").json()['time'].replace(" ", "").replace(":", "-")

def get_host_ip() -> str:
    return requests.get("http://ip.jsontest.com").json()['ip']

def get_servers() -> list[str]:
    with open('myservers.txt') as server_file:
        lines = []
        for line in server_file.readlines():
            lines.append(f"{line.strip()}")
        return lines

if __name__ == '__main__':
    data = {"json": {"time":get_datetime(),
        "ip":get_host_ip(),
        "myservers":get_servers()
        }}
    pprint(data)
    pprint(post_data(data))

