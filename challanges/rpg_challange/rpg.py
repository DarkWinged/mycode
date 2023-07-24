#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import random
from random import seed as seed_random

class Creature(ABC):
     
    @abstractmethod
    def initive(self): pass
   
    @abstractmethod
    def attack(self, target:Creature): pass

    @abstractmethod
    def defend(self, attack:int, damage:int): pass


class Item(ABC):

    @abstractmethod
    def use(self): pass


@dataclass
class Creature_data:
    name: str
    hp: int
    strength: int
    dextarity: int
    constitution: int
    intellegenct: int
    wisdom: int
    charisma: int


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
                return 1
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


@dataclass
class Hero_data:
    armor: Armor
    weapon: Weapon
    potions: list[Consumeable]
    inventory: list[Item]


@dataclass
class Job_data(Creature_data, Hero_data): pass


class Monster(Creature):
    def __init__(self, data: Creature_data):
        self.hp_max = data.hp + data.constitution
        self.hp_current = self.hp_max
        self.strength = data.strength
        self.dextarity = data.dextarity
        self.constitution = data.constitution
        self.intellegenct = data.intellegenct
        self.wisdom = data.wisdom
        self.charisma = data.charisma

    def initive(self):
        return math.floor((100 * random()) % 20) + self.dextarity
   
    def attack(self, target:Creature): 
        attack = math.floor((100 * random()) % 20) + self.strength
        damage = math.floor((100 * random()) % 4) + self.strength
        target.defend(attack, damage)
        
    def defend(self, attack:int, damage:int):
        if self.dextarity <= attack:
            self.hp_current -= damage


class Hero(Creature):
    def __init__(self, data: Job_data):
        self.hp_max = data.hp + data.constitution
        self.hp_current = self.hp_max
        self.strength = data.strength
        self.dextarity = data.dextarity
        self.constitution = data.constitution
        self.intellegenct = data.intellegenct
        self.wisdom = data.wisdom
        self.charisma = data.charisma
        self.armor = data.armor
        self.weapon = data.weapon
        self.potions = data.potions
        self.inventory = data.inventory
 
    def initive(self):
        return math.floor((100 * random()) % 20) + self.dextarity
   
    def attack(self, target:Creature): 
        attack = math.floor((100 * random()) % 20) + self.strength
        if self.weapon is not None:
            damage = self.weapon.use() + self.strength
        else:
            damage = math.floor((100 * random()) % 4) + self.strength
    
        target.defend(attack, damage)
        
    def defend(self, attack:int, damage:int):
        if self.armor is not None:
            defence += self.armor.use(self.dextarity)
        else:
            defence = self.dextarity
        if defence <= attack:
            self.hp_current -= damage
       
    def equip(self, inventory_item: int):
        equipment = self.inventory.pop(inventory_item)
        match type(equipment):
            case type(Armor):
                unequip(self.armor)
                self.armor = equipment
            case type(Weapon):
                unequip(self.weapon)
                self.weapon = equipment
            case type(Consumeable):
                self.potions.append(equipment)
        
    def unequip(self, equipment: Item):
        match type(equipment):
            case type(Armor):
                self.inventory.append(self.armor)
                self.armor = None
            case type(Weapon):
                self.inventory.append(self.weapon)
                self.weapon = None
            case type(Consumeable):
                self.potions.pop(self.potions.index(equipment))

    def use_potion(self, target: Creature, slot: int):
        potion = self.potions.pop[slot]
        if potion.benefical and target is not self:
            choice = get_input('Are you sure you want to do this?\n> ', ['y','n'])
            if choice == 'y':
                target.hp_current += potion.use()
                self.potions.pop(slot)
        elif not potion.benefical and target is self:
            choice = get_input('Are you sure you want to do this?\n> ', ['y','n'])
            if choice == 'y':
                target.hp_current += potion.use()
                self.potions.pop(slot)
        else:
            target.hp_current += potion.use()
            self.potions.pop(slot)


if __name__ == '__main__':
    # Your main code logic goes here
    pass

