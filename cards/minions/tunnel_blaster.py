from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class TunnelBlaster(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 135
        self.classes = []
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 7
        self.taunt = True
        self.enemy = None
        self.hooks["on_attack_pre"].append(self.save_enemy)
        self.hooks["on_defence_pre"].append(self.save_enemy)
        self.hooks["deathrattle"].append(self.damage_on_death)

    def save_enemy(self, attacker):
        self.enemy = attacker.army

    def damage_all(self):
        targets = [t for t in self.army.cards + self.enemy.cards]
        for t in targets:
            t.health_temp_boost -= 3

    def damage_on_death(self, position):
        if self.triplet:
            self.damage_all()
        self.damage_all()