#!/usr/bin/env python3

def get_name() -> str:
    result = input('Who are you?\n').strip()
    if result == '':
        return 'Monty'
    return result

def get_date() -> str:
    result = input('What day of the week is it?\n').strip()
    if result == '':
        return 'Day'
    return result   

if __name__ == '__main__':
    name = get_name()
    day = get_date()
    print(f'Hello, {name}! Happy {day}!') 

