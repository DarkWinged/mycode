import random
from typing import List
from Data_Classes import PlayerData, ArmorData, WeaponData, PotionData, ItemData
from Creature import Creature
from Potion import Potion
from Item import Item, Armor, Weapon


# Logic class for RPG Player
class Player(Creature):
    def __init__(self, player_data: PlayerData):
        super().__init__(player_data)
        self.armor = Armor(player_data.armor) if player_data.armor else None
        self.weapon = Weapon(player_data.weapon) if player_data.weapon else None
        self.potions = [Potion(potion_data) for potion_data in player_data.potions]
        self.inventory_items = self._instantiate_inventory_items(player_data.inventory_items)

    def _instantiate_inventory_items(self, inventory_items_data: List[ItemData]) -> List[Item]:
        inventory_items = []
        for item_data in inventory_items_data:
            if isinstance(item_data, ArmorData):
                inventory_items.append(Armor(item_data))
            elif isinstance(item_data, WeaponData):
                inventory_items.append(Weapon(item_data))
            elif isinstance(item_data, PotionData):
                inventory_items.append(Potion(item_data))
            else:
                inventory_items.append(Item(item_data))

        return inventory_items

    def attack(self, target: Creature):
        attack_value = self.calculate_attack()
        defense_value = target.defend()

        if attack_value >= defense_value:
            damage = self.calculate_damage()
            target.apply_damage(damage)

    def calculate_attack(self) -> int:
        return random.randint(1, 20) + self.strength

    def calculate_damage(self) -> int:
        return random.randint(1, 4) + self.strength

    def defend(self) -> int:
        return 10 + self.dexterity

    def apply_damage(self, damage: int):
        self.hp -= damage
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        elif self.hp < 1:
            self.dead = True

    def use_potion(self, target: Creature, potion_slot: int):
        if 0 <= potion_slot < len(self.potions):
            potion = self.potions.pop(potion_slot)
            potion.use(target)

    def save_state(self):
        potion_ids = {}
        for potion in self.potions:
            if not potion.id in potion_ids.keys():
                potion_ids.append({'id': sum(map(lambda p: p.id == potion.id, self.potions)) })

        inventory_item_ids = {}
        for item in self.inventory_items:
            if not item.id in inventory_item_ids.keys():
                inventory_item_ids.append({'id': sum(map(lambda i: i.id == item.id, self.inventory_items)), 'type': type(item) })

        return {
            'name': self.name,
            'hp': self.max_hp,
            'strength': self.strength,
            'dexterity': self.dexterity,
            'constitution': self.constitution,
            'intelligence': self.intelligence,
            'wisdom': self.wisdom,
            'charisma': self.charisma,
            'armor': self.armor.id if self.armor else None,
            'weapon': self.weapon.id if self.weapon else None,
            'potions': potion_ids,
            'inventory': inventory_item_ids,
        }

