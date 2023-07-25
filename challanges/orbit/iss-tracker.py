#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged
import requests
from pprint import pprint
import time 
import reverse_geocoder as rg

def get_iss_data() -> dict[any]:
    return requests.get('http://api.open-notify.org/iss-now.json').json()

def print_iss_location(location: dict[str,str]):
    position = (location['latitude'], location['longitude'])
    print(f'Lon: {location["longitude"]}\nLat: {location["latitude"]}')
    location = rg.search(position, verbose=False)[0]
    print(f'City/Country: {location["name"]}, {location["cc"]}')

if __name__ == '__main__':
    data = get_iss_data()
    print('CURRENT LOCATION OF THE ISS:')
    print(time.strftime("Timestamp: %Y-%m-%d %H:%M:%S", time.localtime(data['timestamp'])))
    print_iss_location(data['iss_position'])

