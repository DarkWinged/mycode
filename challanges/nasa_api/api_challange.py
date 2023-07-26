#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged
import requests
from pprint import pprint

base_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

def get_bday():
    pprint(requests.get(f"{base_url}&date=2023-01-23").json())

def get_week():
    pprint(requests.get(f"{base_url}&start_date=2023-07-23&end_date=2023-07-30").json())

def get_random(amount: int):
    pprint(requests.get(f"{base_url}&count={amount}").json())


if __name__ == '__main__':
    get_bday()
    get_week()
    get_random(3)

