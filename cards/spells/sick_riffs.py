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
        if self.triplet:
            atk_boost = self.player.level * 2
            hlt_boost = self.player.level * 2
        else:
            atk_boost = self.player.level
            hlt_boost = self.player.level
        target.attack_temp_boost += atk_boost
        target.health_temp_boost += hlt_boost
        for hook in self.player.army.hooks["on_values_change_temp"]:
            hook(target, atk_boost, hlt_boost)
    