from abc import ABC, abstractmethod
from data_types import Armor_data, Weapon_data, Consumeable_data

class Item(ABC):

    @abstractmethod
    def use(self): pass


class Armor(Item):
    def __init__(self, data: Armor_data):
        self.name = ' '.join(data.name.split('_')).capitalize()
        self.defence = data.armor_value
        self.max_dex = data.max_dex

    def use(self, user_dex:int) -> int:
        if self.max_dex:
            return self.defence + (self.max_dex if user_dex > self.max_dex else user_dex )
        return self.defence + user_dex


class Weapon(Item):
    def __init__(self, data: Weapon_data):
        self.name = ' '.join(data.name.split('_')).capitalize()
        self.total_dice = data.dice_count
        self.damge_dice = data.dice_size
        self.damage_mod = data.modifier

    def use(self) -> int:
        total_damage = self.damage_mod
        for dice in range(self.total_dice):
            damage = math.floor((100 * random())%self.damge_dice)
            if damage < 1:
                damage += 1
            total_damage += damage
        return total_damage


class Consumeable(Item):
    def __init__(self, data: Consumeable_data):
        self.name = ' '.join(data.name.split('_')).capitalize()
        self.beneficial = data.beneficial
        self.dice_size = data.dice_size


    def use(self):
        effect = math.floor((100 * random()) % self.dice_size)
        if effect < 1:
            effect = 1
        if self.beneficial:
            return effect
        return -1 * effect

