from dataclasses import dataclass
from typing import List

@dataclass
class CreatureData:
    id: int
    name: str
    level: int
    exp: int
    hp: int
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

@dataclass
class ItemData:
    id: int
    name: str
    item_type: str

@dataclass
class ArmorData(ItemData):
    armor_value: int
    max_dex: int

@dataclass
class WeaponData(ItemData):
    dice_count: int
    dice_size: int
    modifier: int

@dataclass
class PotionData(ItemData):
    beneficial: bool
    dice_size: int
    dice_count: int

@dataclass
class PlayerData(CreatureData):
    user_id: int
    armor: ArmorData
    weapon: WeaponData
    potions: List[PotionData]
    inventory_items: List[ItemData]

