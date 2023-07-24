#!/usr/bin/env python3

"""
James L. Rogers | github.com/DarkWinged
search from all dnd spells and display info on a specific spell
"""

import requests
import json
from pprint import pprint

class URL:
    def __init__(self, url:str):
        self._url = url

    @property
    def url(self) -> str:
        if self._url[-1] == '/': 
            return f'{self._url}'
        return f'{self._url}/'
    
    def append(self, addition: str) -> str:
        if self._url[-1] == '/': 
            return f'{self._url}{addition}'
        return f'{self._url}/{addition}'

def make_request(request: str) -> dict[str, any]:
    response = requests.get(request)
    return response.json()

def search_results(results: list[dict[str, any]], search: str) -> list[dict[str, any]]:
    return [spell for spell in results if search in spell['index']]

def print_results(results: list[dict[str, any]]):
    print(f'Results: {len(results)}')
    for index, spell in enumerate(results):
        if index < 10:
            print(f"\t{spell['name']}")
        else:
            return

def print_all(data: list[any], ending='\n', end_all='\n'):
    for entry in data:
        print(entry, end=ending)
    print(end=end_all)

def print_spell(spell: dict[str:any]):
    print()

    print(f'{spell["name"]}:', end='\t[')
    print(f'level:{spell["level"]}', end='  ')
    print(f'{spell["school"]["name"]}', end='')
    if spell['concentration']:
        print(f' concentration', end= '')
    if spell['ritual']:
        print(f' ritual', end= '')
    print(end='  ')
    print(spell['casting_time'], end='  ')
    print_all(spell['components'], ending='', end_all=']\n')
    if 'M' in spell['components']:
        print(f'\tRequired materials: {spell["material"]}')

    print('\n', end='\t')
    print_all(spell['desc'], ending='\n\t')
    
    print(f'Range: {spell["range"]}')
    if 'area_of_effect' in spell.keys():
        print(f'AoE: {spell["area_of_effect"]["size"]}ft {spell["area_of_effect"]["type"]}')
    if 'damage' in spell.keys():
        if spell['level'] == 0:
            spell_damage_level = '1'
        else:
            spell_damage_level = f"{spell['level']}"
        if 'damage_at_character_level' in spell['damage'].keys():
            print(f'Damage: {spell["damage"]["damage_at_character_level"][spell_damage_level]}', end=' ')
        if 'damage_at_slot_level' in spell['damage'].keys():
            print(f'Damage: {spell["damage"]["damage_at_slot_level"][spell_damage_level]}', end=' ')
        print(f'{spell["damage"]["damage_type"]["name"]} Damage')
    
    if 'dc' in spell.keys():
        print(f'\tSave: {spell["dc"]["dc_type"]["name"]}')
        print(f'\tSpell effect on save: {spell["dc"]["dc_success"]}')
    
    if 'higher_level' in spell.keys():
        print(end='\t')
        print_all(spell['higher_level'])

def search_api(api:URL):
    inital_search = make_request(api.url)['results']
    while True:
        user_input = '-'.join(input('Search for a spell:\n>').lower().split())
        if user_input == 'quit':
            quit()
        search = search_results(inital_search, user_input)
        addresses = [spell['index'] for spell in search]
        if len(search) == 1 and user_input in addresses:
            spell = make_request(api.append(user_input))
            print_spell(spell)
            continue
        if user_input in addresses:
            spell = make_request(api.append(user_input))
            print_spell(spell)
            continue
        if len(search) == 0:
            print('no spells found\nenter \'quit\' to exit')
            continue
        print_results(search)

if __name__ == '__main__':
    dnd_api = URL('https://www.dnd5eapi.co/api/spells')
    search_api(dnd_api)


