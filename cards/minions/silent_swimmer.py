from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.just_keep_swimming import JustKeepSwimming

if TYPE_CHECKING:
    from models.army import Army


class SilentSwimmer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 127
        self.classes = [MinionClass.Naga]
        self.level = 4
        self.base_attack_value = 5
        self.base_health_value = 3
        self.hooks["on_turn_start"].append(self.give_swim)

    def give_swim(self) -> None:
        self.log.debug(f"{self} giving swim to {self.army.player}")
        if self.triplet:
            self.army.player.hand.add(JustKeepSwimming(self.army.player, triplet=True), len(self.army.player.hand))
        else:
            self.army.player.hand.add(JustKeepSwimming(self.army.player), len(self.army.player.hand))
