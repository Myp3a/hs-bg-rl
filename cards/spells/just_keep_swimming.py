from __future__ import annotations
from typing import TYPE_CHECKING

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class JustKeepSwimming(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player, triplet)
        self.spell_id = 8
        self.level = 4
        self.target = None
        self.spellcraft = True

    def play(self, target: Minion) -> None:
        target.feature_overrides["stealth"].append({"state": True, "one_turn": True})
        if self.triplet:
            atk_boost = 6
            hlt_boost = 10
        else:
            atk_boost = 3
            hlt_boost = 5
        target.attack_temp_boost += atk_boost
        target.health_temp_boost += hlt_boost
        for hook in self.player.army.hooks["on_values_change_temp"]:
            hook(target, atk_boost, hlt_boost)
