from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.anglers_lure import AnglersLure

if TYPE_CHECKING:
    from models.army import Army


class DeepSeaAngler(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 33
        self.classes = [MinionClass.Naga]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 2
        self.hooks["on_turn_start"].append(self.give_lure)

    def give_lure(self) -> None:
        if self.triplet:
            self.army.player.hand.add(AnglersLure(self.army.player, triplet=True), len(self.army.player.hand))
        else:
            self.army.player.hand.add(AnglersLure(self.army.player), len(self.army.player.hand))
