from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.minions.game_entity import GameEntity

if TYPE_CHECKING:
    from models.army import Army


class WildfireElemental(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 93
        self.classes = [MinionClass.Elemental]
        self.level = 3
        self.base_attack_value = 6
        self.base_health_value = 3
        self.target_position = None
        self.target_army = None
        self.hooks["on_attack_pre"].append(self.remember_position)
        self.hooks["on_attack_mid"].append(self.attack_adjacent)

    def remember_position(self, target: Minion):
        self.target_position = target.army.index(target)
        self.target_army = target.army

    def damage(self, target, damage):
        fire = GameEntity(self.army)
        fire.base_attack_value = damage
        fire.attack(target)

    def get_target(self, position):
        return self.target_army.cards[position]

    def check_can_be_damaged(self):
        if len(self.target_army.cards) == 0:
            return False, False
        allow_damage_left = False
        allow_damage_right = False
        if self.target_position - 1 > 0 and self.target_position - 1 < len(self.target_army.cards) and self.target_army.cards[self.target_position - 1].health_value > 0:
            allow_damage_left = True
        if self.target_position < 7 and self.target_position < len(self.target_army.cards) and self.target_army.cards[self.target_position].health_value > 0:
            allow_damage_right = True
        return allow_damage_left, allow_damage_right

    def attack_adjacent(self, target: Minion) -> None:
        overdamage = - target.health_value
        if overdamage > 0:
            allow_left, allow_right = self.check_can_be_damaged()
            if allow_left:
                tl = self.get_target(self.target_position - 1)
            if allow_right:
                tr = self.get_target(self.target_position + 1)
            if self.triplet:
                if allow_left:
                    self.damage(tl, overdamage)
                if allow_right:
                    self.damage(tr, overdamage)
            else:
                if allow_left and allow_right:
                    self.damage(random.choice([tl,tr]), overdamage)
                else:
                    if allow_left:
                        self.damage(tl, overdamage)
                    if allow_right:
                        self.damage(tr, overdamage)
