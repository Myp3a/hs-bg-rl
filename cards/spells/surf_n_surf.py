from __future__ import annotations
from typing import TYPE_CHECKING
from cards.minions.crab import Crab

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class SurfNSurf(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player)
        self.target = None
        self.spell_id = 2
        self.triplet = triplet

    def remove_hook(self) -> None:
        self.target.hooks["deathrattle"].remove(self.summon_crab)
        self.target.hooks["on_turn_start"].remove(self.remove_hook)


    def play(self, target: Minion) -> None:
        self.target = target
        target.hooks["deathrattle"].append(self.summon_crab)
        target.hooks["on_turn_start"].append(self.remove_hook)

    def summon_crab(self, position) -> None:
        crab = Crab(self.player.army)
        if self.triplet:
            crab.base_attack_value *= 2
            crab.base_health_value *= 2
            crab.attack_value = crab.base_attack_value
            crab.health_value = crab.base_health_value
            crab.triplet = True
        self.player.army.add(crab, position)
    