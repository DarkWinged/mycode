from peewee import *
from db_tables import db, Creature, PlayerCharacter, Item, Armor, Weapon, Consumable, Potion, InventoryItem
from rpg.Data_Classes import CreatureData, CharacterData, ConsumableData, WeaponData, ArmorData

# Function to add a new consumable
def add_consumable(name: str, beneficial: bool, dice_size: int, dice_count: int):
    new_item, _ = Item.get_or_create(name=name, item_type='Consumable')
    item_id = new_item.id
    Consumable.get_or_create(item_id=item_id, beneficial=beneficial, dice_size=dice_size, dice_count=dice_count)

# Function to add a new weapon
def add_weapon(name: str, dice_count: int, dice_size: int, modifier: int):
    new_item, _ = Item.get_or_create(name=name, item_type='Weapon')
    item_id = new_item.id
    Weapon.get_or_create(item_id=item_id, dice_count=dice_count, dice_size=dice_size, modifier=modifier)

# Function to add a new armor
def add_armor(name: str, armor_value: int, max_dex: int):
    new_item, _ = Item.get_or_create(name=name, item_type='Armor')
    item_id = new_item.id
    Armor.get_or_create(item_id=item_id, armor_value=armor_value, max_dex=max_dex)

# Function to add a new creature
def add_creature(creature_data: CreatureData):
    Creature.get_or_create(**creature_data.to_dict())

# Function to add a new character
def add_character(character_data: CharacterData):
    player_character = PlayerCharacter.get_or_create(**character_data.to_dict())[0]

    # Set inventory items
    inventory_item_ids = {}
    for item in character_data.inventory_items:
        if not item.id in inventory_item_ids.keys():
            inventory_item_ids[item.id] = sum(map(lambda i: i.id == item.id, character_data.inventory_items))

    # Set equipped inventory items
    for item_id, amount in inventory_item_ids.items():
        InventoryItem.get_or_create(player_character=player_character, item_id=item_id, amount=amount)

    # Set equipped potions
    potion_ids = {}
    for potion in character_data.potions:
        if not potion.id in potion_ids.keys():
            potion_ids[potion.id] = sum(map(lambda p: p.id == potion.id, character_data.potions))

    for potion_id, amount in potion_ids.items():
        PotionSlot.get_or_create(player_character=player_character, potion_id=potion_id, amount=amount)

# Function to initialize creatures
def initialize_creatures():
    # Define your creatures here
    creatures = [
        CreatureData(name='Goblin', hp=20, strength=10, dexterity=12, constitution=8, intelligence=6, wisdom=6, charisma=5, level=1, exp=0),
        CreatureData(name='Orc', hp=40, strength=15, dexterity=10, constitution=12, intelligence=7, wisdom=7, charisma=6, level=2, exp=50),
        CreatureData(name='Skeleton', hp=15, strength=8, dexterity=14, constitution=10, intelligence=4, wisdom=4, charisma=3, level=1, exp=25),
        CreatureData(name='Dragon', hp=200, strength=25, dexterity=18, constitution=20, intelligence=15, wisdom=15, charisma=16, level=10, exp=500),
        CreatureData(name='Zombie', hp=30, strength=12, dexterity=6, constitution=15, intelligence=3, wisdom=3, charisma=2, level=1, exp=10),
        # Add more creatures as needed
    ]

    for creature_data in creatures:
        add_creature(creature_data)

# Function to initialize consumables
def initialize_consumables():
    consumables = [
        ConsumableData(name='Health Potion', beneficial=True, dice_size=8, dice_count=2),
        ConsumableData(name='Fire Bomb', beneficial=False, dice_size=6, dice_count=3),
        # Add more consumables as needed
    ]

    for consumable_data in consumables:
        add_consumable(**consumable_data)

# Function to initialize weapons
def initialize_weapons():
    weapons = [
        WeaponData(name='Sword', dice_count=1, dice_size=8, modifier=2),
        WeaponData(name='Axe', dice_count=1, dice_size=10, modifier=1),
        # Add more weapons as needed
    ]

    for weapon_data in weapons:
        add_weapon(**weapon_data)

# Function to initialize armors
def initialize_armors():
    armors = [
        ArmorData(name='Chainmail', armor_value=14, max_dex=2),
        ArmorData(name='Plate', armor_value=18, max_dex=0),
        # Add more armors as needed
    ]

    for armor_data in armors:
        add_armor(**armor_data)

