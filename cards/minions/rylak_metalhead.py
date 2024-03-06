from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RylakMetalhead(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 125
        self.classes = [MinionClass.Beast]
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 4
        self.taunt = True
        self.hooks["deathrattle"].append(self.trigger_battlecries)

    def trigger_battlecries(self, position):
        if position > 0:
            for hook in self.army.cards[position - 1].hooks["battlecry"]:
                hook()
        if position < len(self.army.cards):
            for hook in self.army.cards[position].hooks["battlecry"]:
                hook()
