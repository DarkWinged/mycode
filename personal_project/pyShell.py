#!/usr/bin/python3

import colorama
from colorama import Fore, Style

shell_end = '$'
user_name = 'user'
work_path = '/home/user'
host_name = 'tmux'

def shell() -> str:
    return input(f'{Fore.GREEN}{user_name}:{host_name}{Style.RESET_ALL} {Fore.BLUE}{work_path}{Style.RESET_ALL}{shell_end} ')

if __name__ == '__main__':
    input_txt = ''
    while input_txt != 'exit':
        input_txt = shell()
        match input_txt:
            case 'pwd':
                print(work_path)
            case 'whoami':
                print(user_name)
            case 'hostname':
                print(host_name)
