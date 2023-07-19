#!/usr/bin/env python3

#Stores the player's name and their score.
#Has methods to update and print a playe's score.
class Player:
    def __init__(self):
        name = ''
        while name == '':
            name = input('Who are you?\n>')
        self.name = name
        self.alignment = (0, 0)

    def update_alignment(self, change: tuple[int, int]):
        orderlyness_change, goodness_change = change
        orderlyness, goodness = self.alignment
        goodness += goodness_change
        orderlyness += orderlyness_change
        self.alignment = (orderlyness, goodness)

    def print_alignment(self):
        orderlyness, goodness = self.alignment

        if goodness <= -12:
            goodness = 'super evil'
        elif goodness <= -9:
            goodness = 'evil'
        elif goodness <= -6:
            goodness = 'a little evil'
        elif goodness >= 12:
            goodness = 'super good'
        elif goodness >= 9:
            goodness = 'good'
        elif goodness >= 6:
            goodness = 'a little good'
        else:
            goodness = 'neutal'

        if orderlyness <= -12:
            orderlyness = 'super chaotic'
        elif orderlyness <= -9:
            orderlyness = 'chaotic'
        elif orderlyness <= -6:
            orderlyness = 'a little chaotic'
        elif orderlyness >= 12:
            orderlyness = 'super lawful'
        elif orderlyness >= 9:
            orderlyness = 'lawful'
        elif orderlyness >= 6:
            orderlyness = 'a little lawful'
        else:
            orderlyness = 'neutal'

        print(f'{self.name} is {orderlyness} {goodness}')


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


#Todo: Import question data from *.Json

#initalizes and returns a question list.
"""
new questions can be added by following this template: 
    prompt = 'Blah bla, bla bla... Blah. What do you do?'
    awnsers = {
            'a': ('blah', (orderly: int, goodly: int)),
            'b': ('blah', (orderly: int, goodly: int)),
            'c': ('blah', (orderly: int, goodly: int)),
            'd': ('blah', (orderly: int, goodly: int))
            } 
    questions.append(Question(prompt, awnsers))
"""
def init():
    questions = []
    prompt = 'A young noble is beating their servant for failing some task. What do you do?'
    awnsers = {
            'a': ('beat the noble and save the servant', (-3,3)),
            'b': ('distact the noble alowing the servant to recover', (0,3)),
            'c': ('offer to show the noble how to properly dicipline a servant', (3,0)),
            'd': ('kill the servant to serve as an example to the other servants', (0,-3))
            } 
    questions.append(Question(prompt, awnsers))
    prompt = 'An orphanage is burning. What do you do?'
    awnsers = {
            'a': ('rush in and save the orphans', (-3,3)),
            'b': ('organize the townsfolk to putout the fire', (3,3)),
            'c': ('revel in the destruction', (0,-3)),
            'd': ('start more fires', (-3,-3))
            } 
    questions.append(Question(prompt, awnsers))
    prompt = 'A beggar comes up to you on the side of the road asking for alms. What do you do?'
    awnsers = {
            'a': ('give them a coin', (3,3)),
            'b': ('share your rations', (0,3)),
            'c': ('beat them up', (-3,-3)),
            } 
    questions.append(Question(prompt, awnsers))
    prompt = 'A wizard is asking for fresh bodies for study. What do you do?'
    awnsers = {
            'a': ('accuse him of being a necromancer and report him to the local lord', (3,3)),
            'b': ('steal corpses form the cemetery', (-3,0)),
            'c': ('negotiate a deal with the local lord to "dispose" of the bodies of executed criminals', (3, 0)),
            'd': ('murder an innocent villager', (0,-3))
            } 
    questions.append(Question(prompt, awnsers))
    prompt = 'A dragon is terrorizing a nearby village. What do you do?'
    awnsers = {
            'a': ('gather you allies and slay the dargon', (3,3)),
            'b': ('offer a treasure as tribute to dragon in exchange for the village\s safety', (0,3)),
            'c': ('sacrafice a young prince to the dragon in exchange for power', (0, -3)),
            'd': ('use your bardic charm to seduce the dragon <3', (-3,0))
            } 
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

