#!/usr/bin/env python3

import json
from pprint import pprint

def load_data() -> dict[any]:
    with open('farm_data.json') as farm_data:
        return json.load(farm_data)['farms2']

def init() -> dict[str, list]:
    data = load_data()
    farms = {}
    for farm in data:
        farms[farm['name']]= farm['agriculture']
    return farms

def select_farm(farms: list[str]) -> str:
    farm_selection = [farm.lower() for farm in farms]
    farms = [farm for farm in farms]
    while True:
        pprint(farms)
        selection = input('Select a farm\n>').strip().lower()
        if selection == 'exit':
            quit()
        if selection in farm_selection:
            return farms[farm_selection.index(selection)]
    
def select_agriculture() -> str:
    valid = ['plants', 'animals']
    while True:
        pprint(valid)
        selection = input('Select a agriculture type\n>').strip().lower()
        if selection == 'exit':
            quit()
        if selection in valid:
            return selection

def print_farm(name: str, farm: list[str], agri_type: str):
    print(name)
    plant_kingdom = ['carrots', 'celery', 'bananas', 'apples', 'oranges']
    if agri_type == 'plants':
        for product in [life_from for life_from in farm if life_from in plant_kingdom]:
            print(f'\t{product}')
    elif agri_type == 'animals':
        for product in [life_from for life_from in farm if life_from not in plant_kingdom]:
            print(f'\t{product}')

if __name__ == '__main__':
    farms = init()
    farm = select_farm(farms.keys())
    agri_type = select_agriculture()
    print_farm(farm, farms[farm], agri_type)

