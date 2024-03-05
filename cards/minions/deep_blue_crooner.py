from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.deep_blues import DeepBlues

if TYPE_CHECKING:
    from models.army import Army


class DeepBlueCrooner(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 104
        self.classes = [MinionClass.Naga]
        self.level = 4
        self.base_attack_value = 2
        self.base_health_value = 2
        self.hooks["on_turn_start"].append(self.give_blues)

    def give_blues(self) -> None:
        if self.triplet:
            self.army.player.hand.add(DeepBlues(self.army.player, triplet=True), len(self.army.player.hand))
        else:
            self.army.player.hand.add(DeepBlues(self.army.player), len(self.army.player.hand))
