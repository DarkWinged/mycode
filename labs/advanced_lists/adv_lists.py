#! /usr/bin/env python3
from pprint import pprint

def franchise_format(franchises: list[str, list[str, list[str]]]) -> dict[dict[list[str], str], str]:
    names = [index[0] for index in franchises]
    teams = [index[1:] for index in franchises]
    result = {}
    for index in range(len(names)):
        result[names[index]] = {}
        for team in teams[index]:
            result[names[index]][team[0]] = team[1]
    return result

if __name__ == '__main__':
    inital = [
            ["Marvel",
                ["Avengers",["Iron Man","Captain America","Thor"]],
                ["X-Men",["Wolverine","Cyclops","Storm"]]
            ],
            ["DC Comics",
                ["Justice League",["Superman","Batman","Wonder Woman"]],
                ["Teen Titans",["Robin","Starfire","Raven", "Cyborg", "Beast Boy"]]
            ]
            ]
    results = franchise_format(inital)
#    for franchise in results.keys():
#        for team in results[franchise]:
#            for member in range(len(results[franchise][team])):
#                print(franchise)
#                print(team)
#                print(results[franchise][team][member])

    pprint(results)
    
    print(f'All of the franchises are {[franchise for franchise in results.keys()]}')
    print(f'My favorite franchise is {"Marvel"}')
    print(f'All of the Marvel teams are {[team for team in results["Marvel"].keys()]}')
    print(f'My favorite Marvel team is the Avengers')
    print(f'All of the heros in the Avengers are {results["Marvel"]["Avengers"]}')
    print(f'My favorite hero on the Avengers is {results["Marvel"]["Avengers"][0]}')

