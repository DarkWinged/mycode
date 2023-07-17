#!/usr/bin/env python3
"""Written by James L. Rogers|githum.com/DarkWinged
Asks the user their name and what day it is.
If no input is given it defaults to Monty and Day respectivly.
Prints a greeting to the user and wishes them a happy day.
"""
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

