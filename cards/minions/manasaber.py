from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .cubling import Cubling

if TYPE_CHECKING:
    from models.army import Army


class Manasaber(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 7
        self.classes = [MinionClass.Beast]
        self.level = 1
        self.base_attack_value = 4
        self.base_health_value = 1
        self.hooks["deathrattle"].append(self.summon_cublings)

    def summon_cublings(self, position) -> None:
        for _ in range(2):
            cub = Cubling(self.army)
            if self.triplet:
                cub.triplet = True
            self.log.debug(f"{self} summoning {cub}")
            for hook in cub.hooks["on_get"]:
                hook()
            self.army.add(cub, position)
            for hook in self.army.hooks["on_minion_summon"]:
                hook(cub)