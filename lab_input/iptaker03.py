#!/usr/bin/env python3

def get_name() -> str:
    return input('Who are you?\n').strip()

def get_date() -> str:
    return input('What day of the week is it?\n').strip()

if __name__ == '__main__':
    name = get_name()
    day = get_date()
    print(f'Hello, {name}! Happy {day}!') 

