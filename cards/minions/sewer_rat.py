from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .half_shell import HalfShell

if TYPE_CHECKING:
    from models.army import Army


class SewerRat(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 50
        self.classes = [MinionClass.Beast]
        self.level = 2
        self.base_attack_value = 3
        self.base_health_value = 2
        self.hooks["deathrattle"].append(self.summon_turtle)

    def summon_turtle(self, position) -> None:
        hs = HalfShell(self.army)
        if self.triplet:
            hs.triplet = True
        self.army.add(hs, position)
