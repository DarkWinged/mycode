#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/python3
"""Alta3 Research | RZFeeser@alta3.com
   CHALLENGE 02 - Redesign script to read environmental variables to determine how to run"""

# standard library
import argparse
import os   # allows us to read in environmental variables
import json # the "list" read in from an ENV will look like JSON and needs decoded

## Ping router - returns True or False
def ping_router(hostname):

    response = os.system("ping -c 1 " + hostname)

    #and then check the response...
    if response == 0:
        return True
    else:
        return False

def main():
    #switchlist = ["172.0.1.2", "sw-1", "sw-2", "8.8.8.8"]   # CUSTOMIZE THIS LIST WITH IPs to PING

    # setting environmental variable API_USER to 'student'
    # os.environ['API_USER'] = 'student'

    # try to get the variable IP_TO_PING
    # export IP_TO_PING='["8.8.8.8", "192.168.70.1"]' - set the environmental variable as a list to be decoded
    # unset IP_TO_PING - removes an environmental variable
    switchlist = os.environ.get('IP_TO_PING', '["example.org"]')   # returns example.org in a format to be decoded from "legal json" to python
    switchlist = json.loads(switchlist)  # decode whatever was found from legal JSON to python

    ## Use a loop to check each device for ICMP responses
    print("\n***** STARTING ICMP CHECKING *****")
    for x in switchlist:
        if ping_router(x):
            print(f"IP address {x} is responding to ICMP")
        else:
            print(f"IP address {x} is not responding to ICMP")

if __name__ == "__main__":
    main()


