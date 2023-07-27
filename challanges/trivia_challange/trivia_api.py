#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged
"""Friday Warmup | Returning Data From Complex JSON"""
import menus
import requests
from pprint import pprint
import random
import math
import html

BASE_URL= "https://opentdb.com/api.php"

class Question:
    def __init__(self, q_dict: dict[str,any]):
        self.question_format = q_dict['type']
        self.prompt = html.unescape(q_dict['question'])
        self.awnser = q_dict['correct_answer']
        self.options = []
        self.options.extend(q_dict['incorrect_answers'])
        self.options.append(self.awnser)

    def shuffle(self):
        shuffled = []
        for option in range(len(self.options)):
            index = int(math.floor((100 * random.random()) % len(self.options))) -1
            if index < 0:
                index = 0
            shuffled.append(self.options.pop(index))
        self.options.extend(shuffled)
        
    def ask(self):
        self.shuffle()
        choice = menus.get_input(self.prompt, self.options)
        if choice == self.awnser.lower():
            print('Correct!')
        else:
            print(f'Incorrect...\n\tCorrect awnser: {self.awnser}')

def main():
    catagories = ['General Knowledge', 'Books', 'Film', 'Music', 'Theatre', 'TV', 'Video Games', 'Board Games']
    dificulties = ['Easy', 'Medium', 'Hard']
    question_types = ['Any', 'Multiple', 'T/F']
    url = f'{BASE_URL}?amount=10'
    catagory_selection = menus.get_input('Select a Catagory', catagories, enum=True) + 9
    dificulty_selection = menus.get_input('Select a dificulty level', dificulties)
    q_type = menus.get_input('Select a question type', question_types, enum=True)
    if q_type == 0:
        q_type_selection = ''
    elif q_type == 1:
        q_type_selection = '&type=multiple'
    elif q_type == 2:
        q_type_selection = '&type=boolean'
    url = f'{url}&category={catagory_selection}&difficulty={dificulty_selection}{q_type_selection}'
    # data will be a python dictionary rendered from your API link's JSON!
    print(url)
    data = requests.get(url).json()['results']
    pprint(data)    
    questions = [Question(quest) for quest in data]
    for question in questions:
        question.ask()

if __name__ == "__main__":
    main()

