#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/python3
"""Alta3 Research | RZFeeser@alta3.com
   Writing a script to perform ICMP checks."""

import os
import argparse
import yaml

def convert_yaml(path: str) -> list[str]:
    expanded_path = os.path.expanduser(os.path.normpath(path))
    with open(expanded_path) as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.SafeLoader)

## Ping router - returns True or False
def ping_router(hostname):

    response = os.system("ping -c 1 " + hostname)

    #and then check the response...
    if response == 0:
        return True
    else:
        return False

def main(switchlist: list[str]):
    #switchlist = ["172.0.1.2", "sw-1", "sw-2", "8.8.8.8"]   # CUSTOMIZE THIS LIST WITH IPs to PING

    ## Use a loop to check each device for ICMP responses
    print("\n***** STARTING ICMP CHECKING *****")
    for x in switchlist:
        if ping_router(x):
            print(f"IP address {x} is responding to ICMP")
        else:
            print(f"IP address {x} is not responding to ICMP")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ping a list of IP addresses")
    parser.add_argument("switchlist", nargs='?', type=str, help="String that represents a list of IP addresses to ping")
    parser.add_argument("-y", "--yaml", action="store_true", help="Sets the program to yaml mode where it convers the .yaml at that path to a list of IP addresses")
    args = parser.parse_args()
    if args.yaml:
        switchlist = convert_yaml(args.switchlist)
    else:
        switchlist = args.switchlist.split()
    main(switchlist)


