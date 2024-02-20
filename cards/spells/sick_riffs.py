from __future__ import annotations
from typing import TYPE_CHECKING

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class SickRiffs(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player)
        self.spell_id = 5
        self.triplet = triplet

    def play(self, target: Minion) -> None:
        target.attack_temp_boost += self.player.level
        target.health_temp_boost += self.player.level
        if self.triplet:
            target.attack_temp_boost += self.player.level
            target.health_temp_boost += self.player.level
    