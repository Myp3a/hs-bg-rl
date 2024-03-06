from __future__ import annotations
from typing import TYPE_CHECKING

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class JustKeepSwimming(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player)
        self.spell_id = 8
        self.level = 4
        self.triplet = triplet
        self.target = None
        self.had_stealth = None

    def restore(self) -> None:
        self.target.stealth = self.had_stealth
        self.target.hooks["on_turn_start"].remove(self.restore)

    def try_remove_hook(self) -> None:
        try:
            self.restore()
        except:
            pass

    def play(self, target: Minion) -> None:
        self.had_stealth = target.stealth
        self.target = target
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
        target.stealth = True
        target.hooks["on_turn_start"].append(self.restore)
        target.hooks["on_sell"].append(self.try_remove_hook)
