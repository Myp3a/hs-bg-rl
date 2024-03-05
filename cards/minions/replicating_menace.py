from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .microbot import Microbot

if TYPE_CHECKING:
    from models.army import Army


class ReplicatingMenace(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 87
        self.classes = [MinionClass.Mech]
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 2
        self.magnetic = True
        self.hooks["deathrattle"].append(self.summon_microbots)

    def summon_microbots(self, position):
        for _ in range(3):
            mb = Microbot(self.army)
            if self.triplet:
                mb.triplet = True
            self.army.add(mb, position)
            for hook in self.army.hooks["on_minion_summon"]:
                hook(mb)