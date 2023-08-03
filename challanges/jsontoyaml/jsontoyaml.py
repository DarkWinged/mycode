#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

import requests
import yaml
import argparse
from pprint import pprint
from os import path
URL = 'https://raw.githubusercontent.com/csfeeser/Python/master/data%20sets/favs.json'


def add_new_entry() -> dict[str, str]:
    new_entry = {}
    new_entry['name'] = input('name:') 
    new_entry['movie'] = input('movie:') 
    new_entry['color'] = input('color:') 
    new_entry['ice cream'] = input('ice cream:')
    return new_entry

def write_yaml(data: list[dict[str, str]]):
    file_path = args.path
    if not file_path.endswith('.yaml'):
        file_path = file_path + '.yaml'
    with open(path.expanduser(path.normpath(file_path)), "w") as yaml_file:
        yaml.dump(data, yaml_file)
    
def main():
    data = requests.get(URL).json()
    data.append(add_new_entry())
    write_yaml(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Gets a json from a url then converts it to a yaml file")
    parser.add_argument("path", nargs='?', type=str, help="Path to where the yaml file will be saved.")
    args = parser.parse_args()
    if args.path:
        main()
