#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/python3
import requests
from pprint import pprint

## Define NEOW URL
NEOURL = "https://api.nasa.gov/neo/rest/v1/feed?"

# this function grabs our credentials
# it is easily recycled from our previous script
def returncreds():
    ## first I want to grab my credentials
    with open("/home/student/nasa.creds", "r") as mycreds:
        nasacreds = mycreds.read()
    ## remove any newline characters from the api_key
    nasacreds = "api_key=" + nasacreds.strip("\n")
    return nasacreds

# this is our main function
def main():
    ## first grab credentials
    nasacreds = returncreds()

    ## update the date below, if you like
    startdate = "start_date=2019-11-11"

    ## the value below is not being used in this
    ## version of the script
    # enddate = "end_date=END_DATE"

    # make a request with the request library
    neowrequest = requests.get(NEOURL + startdate + "&" + nasacreds)

    # strip off json attachment from our response
    neodata = neowrequest.json()
    neos = neodata['near_earth_objects']
    hazards = []
    for date in neos.keys():
        for neo in range(len(neos[date])):
            if neos[date][neo]['is_potentially_hazardous_asteroid']:
                hazard = neos[date][neo]
                hazards.append({'name':hazard['name'],
                    'date':date,
                    'estimated_diameter_in_meters':hazard['estimated_diameter']['meters'],
                    'close_approach_data':hazard['close_approach_data']
                    })
    
    for hazard in hazards:
        print('{')
        pprint(hazard['name'])
        pprint(hazard['date'])
        pprint(hazard['estimated_diameter_in_meters'])
        pprint(hazard['close_approach_data'])
        print('}')

    ## display NASAs NEOW data
    #pprint(neodata['near_earth_objects']['2019-11-18'][0].keys())

if __name__ == "__main__":
    main()


