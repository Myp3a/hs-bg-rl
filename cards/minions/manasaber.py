from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .cubling import Cubling

if TYPE_CHECKING:
    from models.army import Army


class Manasaber(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.classes = [MinionClass.Beast]
        self.level = 1
        self.base_attack_value = 4
        self.base_health_value = 1
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["deathrattle"].append(self.summon_cublings)

    def summon_cublings(self, position) -> None:
        for _ in range(2):
            cub = Cubling(self.army)
            if self.triplet:
                cub.triplet = True
                cub.base_attack_value *= 2
                cub.base_health_value *= 2
                cub.attack_value = cub.base_attack_value
                cub.health_value = cub.base_health_value
            self.army.add(cub, position)