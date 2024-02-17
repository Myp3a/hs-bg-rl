from __future__ import annotations
from typing import TYPE_CHECKING
from cards.minions.crab import Crab

from cards.spell import Spell

if TYPE_CHECKING:
    from cards.minion import Minion

class SurfNSurf(Spell):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.target = None

    def play(self, target: Minion) -> None:
        self.target = target
        target.hooks["deathrattle"].append(self.summon_crab)

    def summon_crab(self, position) -> None:
        self.player.army.add(Crab(self.player.army), position)
        self.target.hooks["deathrattle"].remove(self.summon_crab)
    