#!/usr/bin/python3

from getpass import getpass
from colorama import Fore, Style


def shell(user_name: str, host_name: str, work_path: str, shell_end: str) -> str:
    return input(f'{Fore.GREEN}{user_name}:{host_name}{Style.RESET_ALL} {Fore.BLUE}{work_path}{Style.RESET_ALL}{shell_end} ')

def login(passwd: dict[str, str]) -> tuple[str, str, str]:
    logged_in = False
    while logged_in == False:
        login_name = input(f'{host_name} login: ')
        attempts = 3
        while attempts > 0:
            login_passwd = getpass('password: ')
            if passwd[login_name] == login_passwd:
                user_name = login_name
                home_path = f'/home/{user_name}'
                logged_in = True
                break
            print('Login incorrect')
            attempts -= 1
    return user_name, home_path, home_path


if __name__ == '__main__':
    shell_end = '$'
    host_name = 'tmux'
    passwd = {'testuser':'test'}
    user_name, home_path, work_path = login(passwd)
    input_txt = ''
    while input_txt != 'exit':
        input_txt = shell(user_name, host_name, work_path, shell_end)
        match input_txt:
            case 'pwd':
                print(work_path)
            case 'whoami':
                print(user_name)
            case 'hostname':
                print(host_name)
