#!/usr/bin/env python3
"""
James L. Rogers | github.com/DarkWinged
"""

import json

#Stores the player's name and their score.
#Has methods to update and print a playe's score.
class Player:
    def __init__(self):
        name = ''
        while name == '':
            name = input('Who are you?\n>').capitalize()
        self.name = name
        self.alignment = (0, 0)

    def update_alignment(self, change: tuple[int, int]):
        orderlyness_change, goodness_change = change
        orderlyness, goodness = self.alignment
        goodness += goodness_change
        orderlyness += orderlyness_change
        self.alignment = (orderlyness, goodness)

    def format_score(self, value: int, dimension: tuple[str, str]) -> str:
        negative, posative = dimension
        if value <= -12:
            return f'super {negative}'
        elif value <= -9:
            return negative
        elif value <= -6:
            return f'a little {negative}'
        elif value >= 12:
            return f'super {posative}'
        elif value >= 9:
            return posative
        elif value >= 6:
            return f'a little {posative}'
        else:
            return 'neutal'

    def print_alignment(self):
        orderlyness_score, goodness_score = self.alignment
        
        goodness = self.format_score(goodness_score, ['evil','good'])
        orderlyness = self.format_score(orderlyness_score, ['chaotic','lawful'])

        print(f'{self.name}\'s alignment is {orderlyness} {goodness}')


#Stores a prompt and the valid awnsers to the prompt.
#Prompt awnsers also contain score values.
#Has methods that allow a player to awnser the prompt and recieve a score.
class Question:
    def __init__(self, prompt: str, awnsers:dict[str: tuple[str, tuple[int, int]]]):
        self.prompt = prompt
        self.awnsers = awnsers
        self.valid = []
        for key in awnsers.keys():
            self.valid.append(key.lower())

    def awnser_question(self, player: Player):
        invalid = True
        while invalid:
            print(self.prompt)
            for key in self.awnsers.keys():
                print(f'{key}) {self.awnsers[key][0]}')
            player_awnser = input('>').strip().lower()
            if player_awnser in self.valid:
                player.update_alignment(self.awnsers[player_awnser][1])
                invalid = False


#import question data from questions.Json
def import_questions() -> list[any]:
    with open('questions.json') as question_file:
        #pprint(json.load(question_file))
        return json.load(question_file)['questions']

#initalizes and returns a question list.
def init():
    questions = []
    new_questions = import_questions()
    for question in new_questions:
        prompt = question['prompt']
        awnsers = {}
        for key in question['awnsers'].keys():
            awnsers[key] = (question['awnsers'][key][0], (question['awnsers'][key][1][0], question['awnsers'][key][1][1]))
        questions.append(Question(prompt, awnsers))
    return questions


#Consent form must be seigned in the affermative inorder to take the test
def consent_form():
    consent = ''
    while consent != 'y':
        consent = input('WARNING SOME QUESTIONS MY BE UNSUTABLE FOR SOME AUDIENCES\nprocede? (y/n): ').strip().lower()
        if consent == 'n':
            quit()


if __name__ == '__main__':
    print('<----->D&D ALIGNMENT QUIZ<----->')
    consent_form()
    questions = init()
    player = Player()
    for question in questions:
        question.awnser_question(player)
    player.print_alignment()

