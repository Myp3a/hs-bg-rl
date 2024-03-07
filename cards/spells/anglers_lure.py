from __future__ import annotations
from typing import TYPE_CHECKING
from cards.minions.crab import Crab

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class AnglersLure(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player)
        self.target = None
        self.spell_id = 3
        self.level = 2
        self.triplet = triplet
        self.had_taunt = None
        self.spellcraft = True

    def restore(self) -> None:
        self.target.taunt = self.had_taunt
        self.target.hooks["on_turn_start"].remove(self.restore)

    def try_remove_hook(self) -> None:
        try:
            self.restore()
        except:
            pass        

    def play(self, target: Minion) -> None:
        self.target = target
        self.had_taunt = target.taunt
        target.taunt = True
        if self.triplet:
            hlt_boost = 8
        else:
            hlt_boost = 4
        target.health_temp_boost += hlt_boost
        for hook in self.player.army.hooks["on_values_change_temp"]:
            hook(target, 0, hlt_boost)
        target.hooks["on_turn_start"].append(self.restore)
        target.hooks["on_sell"].append(self.try_remove_hook)
    