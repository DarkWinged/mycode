#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

import menues
import creatures
from data_types import Creature_data, Armor_data, Weapon_data, Consumeable_data, Job_data
import json
from pprint import pprint


def load_game_data():
    with open('game_data.json') as data_file:
        data = json.load(data_file)
        return data

def unpack_monster(name: str, data: dict[str,int]) -> Creature_data:
    return Creature_data(name,
            data['hp'],
            data['strength'],
            data['dextarity'],
            data['constitution'],
            data['intellegence'],
            data['wisdom'],
            data['charisma'])

def unpack_job(name: str, data: dict[str,int]) -> Creature_data:
    return Job_data(name=name,
            hp=data['hp'],
            strength=data['strength'],
            dextarity=data['dextarity'],
            constitution=data['constitution'],
            intellegence=data['intellegence'],
            wisdom=data['wisdom'],
            charisma=data['charisma'],
            armor=data['armor'],
            weapon=data['weapon'],
            potions=data['potions'],
            inventory=data['inventory'])

def unpack_armor(name: str, data: dict[str, int]):
    return Armor_data(name,
            data['armor_value'],
            data['max_dex'])

def unpack_weapon(name: str, data: dict[str, any]):
    dice_data = data['dice'].split('d')
    return Weapon_data(name,
            int(dice_data[0]),
            int(dice_data[1]),
            data['modifier'])

def unpack_consumeable(name: str, data: dict[str, any]):
    return Consumeable_data(name,
            data['beneficial'],
            data['dice_size'])

def init():
    data = load_game_data()
    database = {}
    database['monsters'] = {}
    for monster in data['monsters'].keys():
        database['monsters'][monster] = unpack_monster(monster, data['monsters'][monster])

    database['armors'] = {}
    for armor in data['armors'].keys():
        database['armors'][armor] = unpack_armor(armor, data['armors'][armor])
 
    database['weapons'] = {}
    for weapon in data['weapons'].keys():
        database['weapons'][weapon] = unpack_weapon(weapon, data['weapons'][weapon])
  
    database['consumeables'] = {}
    for consumeable in data['consumeables'].keys():
        database['consumeables'][consumeable] = unpack_consumeable(consumeable, data['consumeables'][consumeable])
 
    database['jobs'] = {}
    for job in data['jobs'].keys():
        database['jobs'][job] = unpack_job(job, data['jobs'][job])
    
    return database


def main_menu(database: dict[str, dict[str, any]]):
    menu_options=['new game', 'view database', 'exit']
    while True:
        choice = menues.get_input('!!!RPG GAME!!!', menu_options, enum=True)
        print(choice)
        if choice == 0:
            pass
        elif choice == 1:
            view_database(database)
        elif choice == 2:
            return

def view_database(database: dict[str, dict[str: any]]):
    database_section = menues.get_input('View game data:', list(database.keys()))
    choice = menues.get_input(f'View {database_section.removesuffix("s")} data:', list(database[database_section].keys()))
    pprint(database[database_section][choice])


if __name__ == '__main__':
    confirm = menues.get_input('Would you like to play a game?', ['y','n'])
    if confirm:
       database  = init()
       main_menu(database) 
