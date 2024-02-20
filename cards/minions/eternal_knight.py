from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class EternalKnight(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 34
        self.classes = [MinionClass.Undead]
        self.level = 2
        self.base_attack_value = 4
        self.base_health_value = 1
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["on_death"].append(self.boost_knights)
        self.hooks["on_play"].append(self.get_boost)
        self.hooks["on_sell"].append(self.drop_boost)

    def boost_knights(self) -> None:
        self.army.player.knights_died += 1

    def get_boost(self) -> None:
        self.base_attack_value += self.army.player.knights_died
        self.base_health_value += self.army.player.knights_died
        if self.triplet:
            self.base_attack_value += self.army.player.knights_died
            self.base_health_value += self.army.player.knights_died
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value

    def drop_boost(self) -> None:
        self.base_attack_value = 2
        self.base_health_value = 2
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value