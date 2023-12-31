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

def get_hash(ts: str):
    return hashlib.md5(f'{ts}{private_key}{pub_key}'.encode('utf-8')).hexdigest()

def authenticate_request(url:str):
    time_stamp = str(time())
    hash_key = get_hash(time_stamp)
    return f'{url}&ts={time_stamp}&apikey={pub_key}&hash={hash_key}'

def make_request(authenticated_url:str) -> dict[any]:
    response = requests.get(authenticated_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)

def main():
    base_url='http://gateway.marvel.com/v1/public/'
    user_input = ''
    while user_input != 'quit':
        user_input = input('What would you like to search?\n> ').strip().lower()
        if user_input == 'quit':
            break
        if '?' not in user_input:
            user_input = f'{user_input}?'
        pprint(make_request(authenticate_request(f'{base_url}{user_input}')))



if __name__ == '__main__':
    pub_key, private_key = get_keys()
    main()

