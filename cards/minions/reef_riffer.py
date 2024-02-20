from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.sick_riffs import SickRiffs

if TYPE_CHECKING:
    from models.army import Army


class ReefRiffer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 48
        self.classes = [MinionClass.Naga]
        self.level = 2
        self.base_attack_value = 1
        self.base_health_value = 1
        self.hooks["on_turn_start"].append(self.give_riffs)

    def give_riffs(self) -> None:
        if self.triplet:
            self.army.player.hand.add(SickRiffs(self.army.player, triplet=True), len(self.army.player.hand))
        else:
            self.army.player.hand.add(SickRiffs(self.army.player), len(self.army.player.hand))
