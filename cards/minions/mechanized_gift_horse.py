from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.minions.mechorse import Mechorse

if TYPE_CHECKING:
    from models.army import Army


class MechanizedGiftHorse(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 161
        self.classes = [MinionClass.Mech, MinionClass.Beast]
        self.level = 5
        self.base_attack_value = 4
        self.base_health_value = 4
        self.hooks["deathrattle"].append(self.summon_mechorses)

    def summon_mechorses(self, position) -> None:
        for _ in range(2):
            h = Mechorse(self.army)
            if self.triplet:
                h.triplet = True
            for hook in h.hooks["on_get"]:
                hook()
            self.army.add(h, position)
            for hook in self.army.hooks["on_minion_summon"]:
                hook(h)
