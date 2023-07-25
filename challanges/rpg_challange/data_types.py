from dataclasses import dataclass


@dataclass
class Item_data:
    name: str

@dataclass
class Armor_data(Item_data):
    armor_value: int
    max_dex: int

@dataclass
class Weapon_data(Item_data):
    dice_count: int
    dice_size: int
    modifier: int

@dataclass
class Consumeable_data(Item_data):
    beneficial: bool
    dice_size: int

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
    armor: str
    weapon: str
    potions: list[str]
    inventory: list[str]


@dataclass
class Job_data(Creature_data, Hero_data): pass

