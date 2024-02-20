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
        target.taunt = True
        if self.triplet:
            atk_boost = 2
            hlt_boost = 2
        else:
            atk_boost = 1
            hlt_boost = 1
        target.attack_perm_boost += atk_boost
        target.health_perm_boost += hlt_boost
        for hook in self.player.army.hooks["on_values_change_perm"]:
            hook(target, atk_boost, hlt_boost)