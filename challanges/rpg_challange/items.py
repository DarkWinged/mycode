from abc import ABC, abstractmethod

class Item(ABC):

    @abstractmethod
    def use(self): pass


class Armor(Item):
    def __init__(self, armor_value, max_dex):
        self.defence = armor_value
        self.max_dex = max_dex

    def use(self, user_dex:int) -> int:
        if self.max_dex:
            return self.defence + (self.max_dex if user_dex > self.max_dex else user_dex )
        return self.defence + user_dex


class Weapon(Item):
    def __init__(self, dice_count: int, dice_size: int, modifier: int):
        self.total_dice = dice_count
        self.damge_dice = dice_size
        self.damage_mod = modifier

    def use(self) -> int:
        total_damage = self.damage_mod
        for dice in range(self.total_dice):
            damage = math.floor((100 * random())%self.damge_dice)
            if damage < 1:
                damage += 1
            total_damage += damage
        return total_damage


class Consumeable(Item):
    def __init__(self, effect: bool, dice_size: int):
        self.benefical = effect
        self.dice_size = dice_size


    def use(self):
        effect = math.floor((100 * random()) % self.dice_size)
        if effect < 1:
            effect = 1
        if self.benefical:
            return effect
        return -1 * effect

