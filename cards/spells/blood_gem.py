from __future__ import annotations
from typing import TYPE_CHECKING

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from models.player import Player
    from cards.minion import Minion

class BloodGem(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player, triplet)
        self.spell_id = 0

    def play(self, target: Minion) -> None:
        target.attack_perm_boost += self.player.blood_gem_attack
        target.health_perm_boost += self.player.blood_gem_health
        for hook in self.player.army.hooks["on_values_change_perm"]:
            hook(target, self.player.blood_gem_attack, self.player.blood_gem_health)