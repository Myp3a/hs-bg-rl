from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.minions.smolderwing import Smolderwing

if TYPE_CHECKING:
    from models.army import Army


class GeneralDrakkisath(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 151
        self.classes = [MinionClass.Dragon]
        self.level = 5
        self.base_attack_value = 2
        self.base_health_value = 8
        self.hooks["battlecry"].append(self.give_smolderwing)

    def give_smolderwing(self):
        if self.triplet:
            sw = Smolderwing(self.army)
            for hook in sw.hooks["on_get"]:
                hook()
            self.army.player.hand.add(sw, len(self.army.player.hand.cards))
        sw = Smolderwing(self.army)
        for hook in sw.hooks["on_get"]:
            hook()
        self.army.player.hand.add(sw, len(self.army.player.hand.cards))
