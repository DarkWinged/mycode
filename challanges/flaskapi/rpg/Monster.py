from Creature import Creature
from Data_Classes import MonsterData

class Monster(Creature):
    def __init__(self, monster_data: MonsterData):
        super().__init__(creature_data=monster_data)

