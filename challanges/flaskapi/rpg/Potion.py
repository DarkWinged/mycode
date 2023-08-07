import random
from Data_Classes import PotionData
from Creature import Creature
from Item import Item

class Potion(Item):
    def __init__(self, potion_data: PotionData):
        super().__init__(item_data=potion_data)
        self.beneficial = potion_data.beneficial
        self.dice_size = potion_data.dice_size
        self.dice_count = potion_data.dice_count

    def use(self, target: Creature):
        if self.beneficial:
            # Healing potion
            heal_amount = -self._roll_dice()
            target.apply_damage(heal_amount)
        else:
            # Damage potion
            damage_amount = self._roll_dice()
            target.apply_damage(damage_amount)

    def _roll_dice(self) -> int:
        total_damage = 0
        for _ in range(self.dice_count):
            total_damage += random.randint(1, self.dice_size)
        return total_damage

