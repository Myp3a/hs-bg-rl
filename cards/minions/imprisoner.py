from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .imp import Imp

if TYPE_CHECKING:
    from models.army import Army


class Imprisoner(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.classes = [MinionClass.Demon]
        self.level = 1
        self.base_attack_value = 3
        self.base_health_value = 2
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["deathrattle"].append(self.summon_imp)

    def summon_imp(self, position) -> None:
        imp = Imp(self.army)
        if self.triplet:
            imp.triplet = True
            imp.base_attack_value *= 2
            imp.base_health_value *= 2
            imp.attack_value = imp.base_attack_value
            imp.health_value = imp.base_health_value
        self.army.add(imp, position)