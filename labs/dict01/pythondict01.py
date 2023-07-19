#! /usr/bin/env python3
from pprint import pprint

if __name__ == '__main__':
    character_sheet = {}
    character_sheet.setdefault('stats', {})
    character_sheet['stats'].setdefault('str', 10)
    character_sheet['stats'].setdefault('con', 10)
    character_sheet['stats'].setdefault('dex', 10)
    character_sheet['stats'].setdefault('int', 10)
    character_sheet['stats'].setdefault('wis', 10)
    character_sheet['stats'].setdefault('cha', 10)
    print('Before levelup') 
    pprint(character_sheet)
    level_up = character_sheet
    level_up['stats']['str'] += 2
    level_up['stats']['con'] += 4
    level_up['stats']['dex'] += 6
    level_up['stats']['cha'] += 32
    character_sheet.update(level_up)
    print('After levelup')
    pprint(character_sheet)
    clone = character_sheet.copy()  
    print('My clone')
    pprint(clone)
    clone.update(level_up)
    print('My clone leveled up')
    pprint(clone)


