from peewee import *

db = SqliteDatabase(None)

class BaseModel(Model):
    id = AutoField(primary_key=True)
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(primary_key=True)
    password = CharField()

class Permission(BaseModel):
    name = CharField(unique=True)

class UserPermission(BaseModel):
    user = ForeignKeyField(User, backref='user_permissions')
    permission = ForeignKeyField(Permission, backref='users')

class Creature(BaseModel):
    name = CharField()
    hp = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField()
    constitution = IntegerField()
    intelligence = IntegerField()
    wisdom = IntegerField()
    charisma = IntegerField()
    level = IntegerField()
    exp = IntegerField()

class PlayerCharacter(BaseModel):
    user_id = ForeignKeyField(User, backref='characters')
    name = CharField()
    hp = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField()
    constitution = IntegerField()
    intelligence = IntegerField()
    wisdom = IntegerField()
    charisma = IntegerField()
    level = IntegerField()
    exp = IntegerField()

class Item(BaseModel):
    name = CharField()
    item_type = CharField()

class Armor(BaseModel):
    item_id = ForeignKeyField(Item, backref='armors')
    armor_value = IntegerField()
    max_dex = IntegerField()

class Weapon(BaseModel):
    item_id = ForeignKeyField(Item, backref='weapons')
    dice_count = IntegerField()
    dice_size = IntegerField()
    modifier = IntegerField()

class Consumeable(BaseModel):
    item_id = ForeignKeyField(Item, backref='potions')
    beneficial = BooleanField()
    dice_size = IntegerField()
    dice_count = IntegerField()

class InventoryItem(BaseModel):
    character_id = ForeignKeyField(PlayerCharacter, backref='inventory')
    item_id = ForeignKeyField(Item, backref='inventory_items')
    amount = IntegerField()

class PotionSlot(BaseModel):
    character_id = ForeignKeyField(PlayerCharacter, backref='potion_slots')
    item_id = ForeignKeyField(Potion, backref='potion_slots')
    amount = IntegerField()

