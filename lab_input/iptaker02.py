#!/usr/bin/env python3

def get_ip():
    ip = input('Please enter an PIv4 IP address:')
    print(f'You told me the IPv4 address is: {ip}')

def get_vendor():
    vendor = input('Please enter the vendor name:')
    print(f'You told me the vendor name is: {vendor}')

if __name__  == '__main__':
    get_ip()
    get_vendor()

