#!/usr/bin/env python3

class Player:
    def __init__(self):
        self.name = input('Who are you?\n>')
        self.alignment = (0, 0)

    def update_alignment(self, change: tuple[int, int]):
        goodness_change, orderlyness_change = change
        goodness, orderlyness = self.alignment
        goodness += goodness_change
        orderlyness += orderlyness_change
        self.alignment = (goodness, orderlyness)

    def print_alignment(self):
        goodness, orderlyness = self.alignment
        if goodness <= -15:
            goodness = 'super evil'
        elif goodness <= -10:
            goodness = 'evil'
        elif goodness <= -5:
            goodness = 'a little evil'
        elif goodness >= 15:
            goodness = 'super good'
        elif goodness >= 10:
            goodness = 'good'
        elif goodness >= 5:
            goodness = 'a little good'
        else:
            goodness = 'neutal'

        if orderlyness <= -15:
            orderlyness = 'super chaotic'
        elif orderlyness <= -10:
            orderlyness = 'chaotic'
        elif orderlyness <= -5:
            orderlyness = 'a little chaotic'
        elif orderlyness >= 15:
            orderlyness = 'super lawful'
        elif orderlyness >= 10:
            orderlyness = 'lawful'
        elif orderlyness >= 5:
            orderlyness = 'a little lawful'
        else:
            orderlyness = 'neutal'

        print(f'{self.name} is {orderlyness} {goodness}')


class Question:
    def __init__(self, prompt: str, awnsers:dict[str: tuple[str, tuple[int, int]]]):
        self.prompt = prompt
        self.awnsers = awnsers

    def awnser_question(self, player: Player):
        invalid = True
        valid = ['a', 'b', 'c', 'd']
        while invalid:
            print(self.prompt)
            for key in self.awnsers.keys():
                print(f'{key}) {self.awnsers[key][0]}')
            player_awnser = input('>')
            if player_awnser.lower() in valid:
                player.update_alignment(self.awnsers[player_awnser][1])
                invalid = False

def init():
    questions = []
    prompt = 'A young noble is beating their servant for failing some task. What do you do?'
    awnsers = {
            'a': ('beat the noble and save the servant', (5,-5)),
            'b': ('distact the noble alowing the servant to recover', (5,0)),
            'c': ('offer to show the noble how to properly dicipline a servant', (0,5)),
            'd': ('kill the servant to server as an example to the other servants', (-5,0))
            } 
    questions.append(Question(prompt, awnsers))
    prompt = 'An orphanage is burning. What do you do?'
    awnsers = {
            'a': ('rush in and save the orphans', (5,-5)),
            'b': ('organize the townsfolk to putout the fire', (5,5)),
            'c': ('revel in the destruction', (-5,0)),
            'd': ('start more fires', (-5,-5))
            } 
    questions.append(Question(prompt, awnsers))
    prompt = 'A beggar comes up to you on the side of the road asking for alms. What do you do?'
    awnsers = {
            'a': ('give them a coin', (5,5)),
            'b': ('share your rations', (5,0)),
            'c': ('beat them up', (-5,-5)),
            'd': ('ignore them', (0,0))
            } 
    questions.append(Question(prompt, awnsers))
    return questions

if __name__ == '__main__':
    questions = init()
    player = Player()
    for question in questions:
        question.awnser_question(player)
    player.print_alignment()

