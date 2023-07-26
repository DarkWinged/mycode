#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/python3
import requests
import math
from pprint import pprint

## Define NEOW URL
NEOURL = "https://api.nasa.gov/neo/rest/v1/feed?"


def estimated_sphere_volume(min_diameter, max_diameter):
    # Calculate the average diameter
    avg_diameter = (min_diameter + max_diameter) / 2.0

    # Calculate the radius
    radius = avg_diameter / 2.0

    # Calculate the volume of the sphere
    volume = (4/3) * math.pi * (radius ** 3)

    return volume


def calculate_rank(volume, speed_kph, miss_distance_k):
    # Define weights for each criterion
    volume_weight = 0.4
    speed_weight = 0.3
    distance_weight = 0.3

    # Calculate the rank score
    rank_score = (
        volume_weight * volume +
        speed_weight * (1 / speed_kph) +
        distance_weight * (1 / miss_distance_k)
    )

    return rank_score

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
                diameter = hazard['estimated_diameter']['meters']
                volume = estimated_sphere_volume(diameter['estimated_diameter_min'], diameter['estimated_diameter_max'])
                hazards.append({'name':hazard['name'],
                    'date':date,
                    'estimated_diameter_in_meters':diameter,
                    'estimated_volume': volume,
                    'close_approach_data':hazard['close_approach_data'][0],
                    'threat': calculate_rank(volume,
                        float(hazard['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
                        float(hazard['close_approach_data'][0]['miss_distance']['kilometers']))
                    })
               
    
    sorted_hazards = sorted(hazards, key=lambda x: x['threat'], reverse=True)
    '''for hazard in sorted_hazards:
        print('{')
        pprint(hazard['name'])
        pprint(hazard['date'])
        pprint(hazard['threat'])
        pprint(hazard['estimated_diameter_in_meters'])
        pprint(hazard['estimated_volume'])
        pprint(hazard['close_approach_data'])
        print('}')'''
    pprint(sorted_hazards[0])

    ## display NASAs NEOW data
    #pprint(neodata['near_earth_objects']['2019-11-18'][0].keys())

if __name__ == "__main__":
    main()


