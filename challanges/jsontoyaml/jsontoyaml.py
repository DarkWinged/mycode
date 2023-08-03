#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

import requests
import yaml
import argparse
from pprint import pprint
from os import path
URL = 'https://raw.githubusercontent.com/csfeeser/Python/master/data%20sets/favs.json'


def add_new_entry() -> dict[str, str]:
    new_entry = {
        'name': input('\tname:'), 
        'movie': input('\tmovie:'), 
        'color': input('\tcolor:'), 
        'ice cream': input('\tice cream:')}    
    return new_entry

def write_yaml(data: list[dict[str, str]]):
    file_path = args.path
    if not file_path.endswith('.yaml'):
        file_path = file_path + '.yaml'
    with open(path.expanduser(path.normpath(file_path)), "w") as yaml_file:
        yaml.dump(data, yaml_file, sort_keys=True)
    
def main():
    data = requests.get(URL).json()
    for entry in range(args.new_entries):
        print(f'- {entry}:')
        data.append(add_new_entry())
    write_yaml(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Gets a json from a url then converts it to a yaml file")
    parser.add_argument("path", nargs='?', type=str, help="Path to where the yaml file will be saved.")
    parser.add_argument('-n', '--new_entries', type=int, default=1, help='Number of new entries to add to the data')
    args = parser.parse_args()
    if args.path and args.new_entries > 0:
        main()
