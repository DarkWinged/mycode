#! /usr/bin/env python3
from os import listdir as ls
from os.path import isdir as isdir
from os import getcwd as cwd
from pprint import pprint
import getpass
import shutil

def repath(locations: list[str]) -> str:
    result = ''
    for location in location:
        result = f'/{location}'
    return result

def get_parent_dir(path: str) -> str:
    path_locations = path.split('/')
    cwd_locations = cwd().split('/')

    while '..' in path_locations:
        path_locations.pop(0)
        cwd_locations.pop()
    
    cwd_locations.extend(path_locations)
    return repath(cwd_locations)

def format_path(path: str):
    if path.startswith('/'):
            return path
    elif path.startswith('~'): 
        return f"/home/{getpass.getuser()}/{path.removeprefix('~/')}"
    elif path.startswith('.'):
        return f'{cwd()}/{path.removeprefix("./")}'
    elif path.startswith('..'):
        return f'{cwd()}/{path}'
    else:
        return f'{cwd()}/{path}'

def copy_files(source: str, destenation: str):
    files = [file for file in ls(source) if not isdir(f'{source}{file}')]

    while True:
        pprint(files)
        user_input = input('Would you like to copy these files (y/n)\n> ').strip().lower()
        if user_input == 'y':
            break
        elif user_input == 'n':
            quit()

    for file in files:
        file_path = f'{source}{file}'
        shutil.copy(file_path, f'{destenation}/{file}')

if __name__ == '__main__':
    source = ''
    while not isdir(source):
        directory = input('enter a source directory path:\n> ')
        source = format_path(directory)
    
    destenation = ''
    while not isdir(destenation) and source != destenation:
        directory = input('enter a destenation directory path:\n> ')
        destenation = format_path(directory)

    copy_files(source, destenation)
