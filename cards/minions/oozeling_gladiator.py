from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion
from cards.spells.slimy_shield import SlimyShield

if TYPE_CHECKING:
    from models.army import Army


class OozelingGladiator(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 46
        self.classes = []
        self.level = 2
        self.base_attack_value = 1
        self.base_health_value = 2
        self.hooks["battlecry"].append(self.give_slimy_shields)

    def give_slimy_shields(self) -> None:
        if self.triplet:
            self.army.player.hand.add(SlimyShield(self.army.player, triplet=True), len(self.army.player.hand))
        else:
            self.army.player.hand.add(SlimyShield(self.army.player), len(self.army.player.hand))

