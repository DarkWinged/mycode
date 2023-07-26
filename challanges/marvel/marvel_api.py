#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged
import requests
import hashlib
from os import path
from time import time
from pprint import pprint

def get_keys() -> tuple[str,str]:
    with open(path.expanduser("~/.marvel.creds")) as creds:
        pub_key = creds.readline().strip()
        private_key = creds.readline().strip()
        return pub_key, private_key

def get_hash(ts: str, private: str, public: str):
    return hashlib.md5(f'{ts}{private}{public}'.encode('utf-8')).hexdigest()

def authenticate_request(url:str):
    pub_key, private_key = get_keys()
    time_stamp = str(time())
    hash_key = get_hash(time_stamp, private_key, pub_key)
    authed_url = f'{url}&ts={time_stamp}&apikey={pub_key}&hash={hash_key}'
    print(authed_url)
    return authed_url

def make_request(authenticated_url:str) -> dict[any]:
    response = requests.get(authenticated_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)

def main():
    base_url='http://gateway.marvel.com/v1/public/'
    pprint(make_request(authenticate_request(base_url+'comics'+'?')))


if __name__ == '__main__':
    main()

