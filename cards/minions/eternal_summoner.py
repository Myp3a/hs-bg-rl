from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .eternal_knight import EternalKnight

if TYPE_CHECKING:
    from models.army import Army


class EternalSummoner(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 186
        self.classes = [MinionClass.Elemental]
        self.level = 6
        self.base_attack_value = 8
        self.base_health_value = 1
        self.base_rebirth = True
        self.hooks["deathrattle"].append(self.summon_knight)

    def summon_knight(self, position):
        k = EternalKnight(self.army)
        for hook in k.hooks["on_get"]:
            hook()
        for hook in k.hooks["on_play"]:
            hook()
        if len(self.army.cards) == 7:
            return
        self.army.add(k, position)
