#!/usr/bin/env python3
"""
James L. Rogers | github.com/DarkWinged
solution to lab_35
"""


def load_data() -> list[str]:
    with open('keystone.common.wsgi') as file:
        return file.readlines()

def process_data(data: list[str]) -> tuple[int,list[str],int]:
    fail_ip = []
    sucess = 0
    
    for entry in data:
        if 'failed' in entry:
            fail_ip.append(entry.split()[-1])
        elif 'POST' in entry:
            sucess += 1

    return fail_ip, sucess


if __name__ == "__main__":
    ips, sucesses = process_data(load_data())
    print(f'posts: {sucesses}')
    print(f'authentication failures: {len(ips)}')
    for ip in ips:
        print(f' {ip}')

