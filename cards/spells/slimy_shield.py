from __future__ import annotations
from typing import TYPE_CHECKING

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class SlimyShield(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player)
        self.spell_id = 4
        self.triplet = triplet

    def play(self, target: Minion) -> None:
        target.attack_perm_boost += 1
        target.health_perm_boost += 1
        target.taunt = True
        if self.triplet:
            target.attack_perm_boost += 1
            target.health_perm_boost += 1