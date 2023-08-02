#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/python3
"""Alta3 Research | RZFeeser@alta3.com
   Writing a script to perform ICMP checks."""

import os
import argparse

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
    args = parser.parse_args()
    switchlist = args.switchlist.split()
    main(switchlist)


