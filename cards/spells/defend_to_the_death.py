from __future__ import annotations
from typing import TYPE_CHECKING

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class DefendToTheDeath(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player)
        self.spell_id = 6
        self.level = 2
        self.triplet = triplet
        self.target = None

    def restore(self) -> None:
        self.target.hooks["on_death"].remove(self.add_health)
        self.target.hooks["on_turn_start"].remove(self.restore)

    def play(self, target: Minion) -> None:
        self.target = target
        if self.triplet:
            hlt_boost = 2
        else:
            hlt_boost = 1
        self.target.health_temp_boost += hlt_boost
        for hook in self.player.army.hooks["on_values_change_temp"]:
            hook(self.target, 0, hlt_boost)
        self.target.hooks["on_death"].append(self.add_health)
        self.target.hooks["on_turn_start"].append(self.restore)

    def add_health(self):
        if self.triplet:
            hlt_boost = 2
        else:
            hlt_boost = 1
        self.target.attack_perm_boost += hlt_boost
        for hook in self.player.army.hooks["on_values_change_perm"]:
            hook(self.target, 0, hlt_boost)
    