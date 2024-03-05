from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class BladeCollector(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 101
        self.classes = [MinionClass.Pirate]
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 2
        self.target_position = None
        self.target_army = None
        self.hooks["on_attack_pre"].append(self.remember_position)
        self.hooks["on_attack_mid"].append(self.attack_adjacent)

    def remember_position(self, target: Minion):
        self.target_position = target.army.index(target)
        self.target_army = target.army

    def damage_left(self, damage):
        self.target_army.cards[self.target_position-1].health_temp_boost -= damage

    def damage_right(self, damage):
        self.target_army.cards[self.target_position+1].health_temp_boost -= damage

    def check_can_be_damaged(self):
        if len(self.target_army.cards) == 0:
            return False, False
        allow_damage_left = False
        allow_damage_right = False
        if self.target_position - 1 > 0 and self.target_position - 1 < len(self.target_army.cards) and self.target_army.cards[self.target_position - 1].health_value > 0:
            allow_damage_left = True
        if self.target_position + 1 < 7 and self.target_position + 1 < len(self.target_army.cards) and self.target_army.cards[self.target_position + 1].health_value > 0:
            allow_damage_right = True
        return allow_damage_left, allow_damage_right

    def attack_adjacent(self, target: Minion) -> None:
        allow_left, allow_right = self.check_can_be_damaged()
        if allow_left:
            self.damage_left(self.attack_value)
        if allow_right:
            self.damage_right(self.attack_value)
