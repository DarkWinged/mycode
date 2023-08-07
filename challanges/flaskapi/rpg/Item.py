from Data_Classes import ItemData, ArmorData, WeaponData


class Item:
    def __init__(self, item_data: ItemData):
        self.id = item_data.id
        self.name = item_data.name


class Armor(Item):
    def __init__(self, armor_data: ArmorData):
        super().__init__(item_data=armor_data)
        self.armor_value = armor_data.armor_value
        self.max_dex = armor_data.max_dex

    def calculate_defense(self, dex: int) -> int:
        max_dex = self.max_dex
        armor_value = self.armor_value

        if dex > max_dex:
            dex = max_dex

        return armor_value + dex


class Weapon(Item):
    def __init__(self, weapon_data: WeaponData):
        super().__init__(item_data=weapon_data)
        self.dice_count = weapon_data.dice_count
        self.dice_size = weapon_data.dice_size
        self.modifier = weapon_data.modifier

    def calculate_attack(self, str_value: int) -> int:
        return self._roll_dice() + str_value + self.modifier

    def calculate_damage(self, str_value: int) -> int:
        return self._roll_dice() + str_value

    def _roll_dice(self) -> int:
        return random.randint(1, self.dice_size)

