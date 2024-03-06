from __future__ import annotations
from typing import TYPE_CHECKING
from cards.minions.crab import Crab
import sys
from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class SurfNSurf(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player)
        self.target = None
        self.spell_id = 2
        self.level = 1
        self.triplet = triplet

    def remove_hook(self) -> None:
        # should always fire on turn start
        self.target.hooks["deathrattle"].remove(self.summon_crab)
        self.target.hooks["on_turn_start"].remove(self.remove_hook)

    def try_remove_hook(self) -> None:
        # additional check on sell in case of played spell and then selling
        try:
            self.remove_hook()
        except:
            pass

    def play(self, target: Minion) -> None:
        self.target = target
        target.hooks["deathrattle"].append(self.summon_crab)
        target.hooks["on_turn_start"].append(self.remove_hook)
        target.hooks["on_sell"].append(self.try_remove_hook)

    def summon_crab(self, position) -> None:
        crab = Crab(self.player.army)
        if self.triplet:
            crab.triplet = True
        self.player.army.add(crab, position)
        for hook in self.player.army.hooks["on_minion_summon"]:
            hook(crab)