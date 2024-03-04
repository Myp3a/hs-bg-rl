from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .helping_hand import HelpingHand

if TYPE_CHECKING:
    from models.army import Army


class HandlessForsaken(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 73
        self.classes = [MinionClass.Undead]
        self.level = 3
        self.base_attack_value = 2
        self.base_health_value = 1
        self.hooks["deathrattle"].append(self.summon_hand)

    def summon_hand(self, position):
        h = HelpingHand(self.army)
        if self.triplet:
            h.triplet = True
        self.army.add(h, position)