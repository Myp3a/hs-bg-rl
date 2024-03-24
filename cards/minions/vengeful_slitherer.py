from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.defend_to_the_death import DefendToTheDeath

if TYPE_CHECKING:
    from models.army import Army


class VengefulSlitherer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 92
        self.classes = [MinionClass.Naga]
        self.level = 3
        self.base_attack_value = 5
        self.base_health_value = 1
        self.hooks["on_turn_start"].append(self.give_defend)

    def give_defend(self) -> None:
        self.log.debug(f"{self} giving defend to {self.army.player}")
        if self.triplet:
            self.army.player.hand.add(DefendToTheDeath(self.army.player, triplet=True), len(self.army.player.hand))
        else:
            self.army.player.hand.add(DefendToTheDeath(self.army.player), len(self.army.player.hand))
