from __future__ import annotations
from typing import TYPE_CHECKING
from cards.minions.crab import Crab

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class AnglersLure(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player)
        self.target = None
        self.spell_id = 3
        self.triplet = triplet
        self.had_taunt = None

    def restore(self) -> None:
        self.target.taunt = self.had_taunt
        self.target.health_value -= 4
        if self.triplet:
            self.target.health_value -= 4

    def play(self, target: Minion) -> None:
        self.target = target
        self.had_taunt = target.taunt
        target.taunt = True
        target.health_value += 4
        if self.triplet:
            target.health_value += 4
        target.hooks["on_turn_start"].append(self.restore)
    