from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .mechapony import Mechapony

if TYPE_CHECKING:
    from models.army import Army


class Mechorse(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 162
        self.classes = [MinionClass.Mech, MinionClass.Beast]
        self.level = 1
        self.base_attack_value = 2
        self.base_health_value = 2
        self.hooks["deathrattle"].append(self.summon_mechapony)

    def summon_mechapony(self, position) -> None:
        for _ in range(2):
            h = Mechapony(self.army)
            if self.triplet:
                h.triplet = True
            self.log.debug(f"{self} summoning {h}")
            for hook in h.hooks["on_get"]:
                hook()
            self.army.add(h, position)
            for hook in self.army.hooks["on_minion_summon"]:
                hook(h)
