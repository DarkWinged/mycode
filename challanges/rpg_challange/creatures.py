from __future__ import annotations
from abc import ABC, abstractmethod
import data_types
import menus
from random import random
from random import seed as seed_random


class Creature(ABC):
     
    @abstractmethod
    def initive(self): pass
   
    @abstractmethod
    def attack(self, target:Creature): pass

    @abstractmethod
    def defend(self, attack:int, damage:int): pass


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
        self.armor = None
        self.weapon = None
        self.potions = []
        self.inventory = []
 
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
            choice = menus.get_input('Are you sure you want to do this?\n> ', ['y','n'])
            if choice == 'y':
                target.hp_current += potion.use()
                self.potions.pop(slot)
        elif not potion.benefical and target is self:
            choice = menus.get_input('Are you sure you want to do this?\n> ', ['y','n'])
            if choice == 'y':
                target.hp_current += potion.use()
                self.potions.pop(slot)
        else:
            target.hp_current += potion.use()
            self.potions.pop(slot)


