from __future__ import annotations
from typing import TYPE_CHECKING

from functools import partial
from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class DefendToTheDeath(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player)
        self.spell_id = 6
        self.level = 2
        self.triplet = triplet

    def play(self, target: Minion) -> None:
        if self.triplet:
            hlt_boost = 2
        else:
            hlt_boost = 1
        target.health_temp_boost += hlt_boost
        for hook in self.player.army.hooks["on_values_change_temp"]:
            hook(target, 0, hlt_boost)
        target.hooks["on_death"].append(partial(self.add_health, target=target))

    def add_health(self, target=None):
        if self.triplet:
            hlt_boost = 2
        else:
            hlt_boost = 1
        target.attack_perm_boost += hlt_boost
        for hook in self.player.army.hooks["on_values_change_perm"]:
            hook(target, 0, hlt_boost)
    