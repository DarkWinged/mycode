import random
from Data_Classes import CreatureData

# Logic class for RPG Creature
class Creature:
    def __init__(self, creature_data: CreatureData):
        self.name = creature_data.name
        self.hp = creature_data.hp
        self.max_hp = creature_data.hp
        self.strength = creature_data.strength
        self.dexterity = creature_data.dexterity
        self.constitution = creature_data.constitution
        self.intelligence = creature_data.intelligence
        self.wisdom = creature_data.wisdom
        self.charisma = creature_data.charisma
        self.dead = False

    def defend(self) -> int:
        return 10 + self.dexterity

    def calculate_attack(self) -> int:
        return random.randint(1, 20) + self.strength

    def calculate_damage(self) -> int:
        return random.randint(1, 4) + self.strength

    def apply_damage(self, damage: int):
        self.hp -= damage
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        elif self.hp < 1:
            self.dead = True

