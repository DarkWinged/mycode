#!/usr/bin/env python3

from pprint import pprint

def init() -> dict[any, any]:
    return {
        "Name": 'Iroh',
        "Nation": "Fire",
        "Relatives": ["Zuko - Nephew", "Ozai - Brother", "Lu Ten - Son (Deceased)", "Azulon - Father", "Ilah - Mother"],
        "Bending element" : "Fire",
        "Voiced by" : ["Mako - books 1 & 2", "Greg Baldwin - book 3"],
        "Created by" : ["Michael Dante DiMartino", "Bryan Konietzko"]
        }


def get_input() -> tuple[any, bool]:
    num = input('Choose an entry to edit\n>')
    num_strs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    is_int = False

    for num_str in num_strs:
        if num_str in num:
            num = int(num)
            is_int = True
            break
    
    return num, is_int

def print_menu(person: dict[any, any]):
    for index, key in enumerate(person.keys()):
        print(f'{index})\t{key}')

def new_entry(person: dict[any], key: str=None) -> dict[any]:
    if key is None:
        key = input('What is the name of the new entry?\n>')
    value = input('What is the value of the entry?\n>')
    person.setdefault(key,value)
    return person

def update_entry(person: dict[any], key:str) -> dict[any]:
    pprint(person[key])
    value = input('What is the new value of the entry\n>')
    person.update({key:value})
    return person

def edit_element(input_key:any, input_type: bool, person: dict[any, any]) -> dict[any, any]:
    if input_type:
        if input_key in person.keys():
            key = person.keys[input_key]
            return update_entry(person, key)
        return new_entry(person)
    if input_key in person.keys():
        return update_entry(person, input_key)
    return new_entry(person, key=input_key)

if __name__ == '__main__':
    person = init()
    print_menu(person)
    key, key_type = get_input()
    person = edit_element(key, key_type, person)
    pprint(person)

