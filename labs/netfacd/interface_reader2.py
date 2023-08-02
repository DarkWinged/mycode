#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/env python3

import netifaces
import argparse

def main():
    for i in netifaces.interfaces():
        print('\n****** details of interface - ' + i + ' ******')
        try:
            if args.mac:
                print('MAC: ', end='') # This print statement will always print MAC without an end of line
                print((netifaces.ifaddresses(i)[netifaces.AF_LINK])[0]['addr']) # Prints the MAC address
            if args.ip:
                print('IP: ', end='')  # This print statement will always print IP without an end of line
                print((netifaces.ifaddresses(i)[netifaces.AF_INET])[0]['addr']) # Prints the IP address
        except:          # This is a new line
            print('Could not collect adapter information') # Print an error message


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pints ip and mac address of the host machine's interfaces.")
    parser.add_argument("-i", "--ip", action="store_true", help="Sets the program to print the ip address.")
    parser.add_argument("-m", "--mac", action="store_true", help="Sets the program to print the mac address.")
    args = parser.parse_args()

    if args.ip or args.mac:
        main()
    else:
        print('Error: no arguments set. Use -h or --help to view usage')