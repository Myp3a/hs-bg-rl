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
        self.hooks["on_death"].append(self.boost_knights)
        self.hooks["on_get"].append(self.get_boost)
        self.hooks["on_lose"].append(self.drop_boost)

    def boost_knights(self) -> None:
        self.log.debug(f"{self} boosting knights_died for {self.army.player}")
        self.army.player.knights_died += 1

    def get_boost(self) -> None:
        self.base_attack_value += self.army.player.knights_died
        self.base_health_value += self.army.player.knights_died
        if self.triplet:
            self.base_attack_value += self.army.player.knights_died
            self.base_health_value += self.army.player.knights_died
        self.log.debug(f"{self} got boosted")

    def drop_boost(self) -> None:
        self.base_attack_value = 2
        self.base_health_value = 2
