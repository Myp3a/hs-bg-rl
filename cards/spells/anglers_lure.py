from __future__ import annotations
from typing import TYPE_CHECKING

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class AnglersLure(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player, triplet)
        self.target = None
        self.spell_id = 3
        self.level = 2
        self.spellcraft = True 

    def play(self, target: Minion) -> None:
        self.target = target
        target.feature_overrides["taunt"].append({"state": True, "one_turn": True})
        if self.triplet:
            hlt_boost = 8
        else:
            hlt_boost = 4
        target.health_temp_boost += hlt_boost
        for hook in self.player.army.hooks["on_values_change_temp"]:
            hook(target, 0, hlt_boost)
    