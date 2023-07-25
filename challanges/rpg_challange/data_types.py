from dataclasses import dataclass
from items import Item, Armor, Weapon, Consumeable

@dataclass
class Creature_data:
    name: str
    hp: int
    strength: int
    dextarity: int
    constitution: int
    intellegence: int
    wisdom: int
    charisma: int

@dataclass
class Hero_data:
    armor: Armor
    weapon: Weapon
    potions: list[Consumeable]
    inventory: list[Item]


@dataclass
class Job_data(Creature_data, Hero_data): pass

