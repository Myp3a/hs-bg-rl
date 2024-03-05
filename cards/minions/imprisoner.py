from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .imp import Imp

if TYPE_CHECKING:
    from models.army import Army


class Imprisoner(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 5
        self.classes = [MinionClass.Demon]
        self.level = 1
        self.base_attack_value = 3
        self.base_health_value = 2
        self.hooks["deathrattle"].append(self.summon_imp)

    def summon_imp(self, position) -> None:
        imp = Imp(self.army)
        if self.triplet:
            imp.triplet = True
        self.army.add(imp, position)
        for hook in self.army.hooks["on_minion_summon"]:
            hook(imp)