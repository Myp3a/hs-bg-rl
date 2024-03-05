from __future__ import annotations
from functools import partial
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SoreLoser(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 89
        self.classes = [MinionClass.Undead]
        self.level = 3
        self.base_attack_value = 2
        self.base_health_value = 4
        self.hooks["on_play"].append(self.put_hook_existing)
        self.hooks["on_death"].append(self.decrease_boost)
        self.hooks["on_turn_start"].append(self.reset_boost)
        
    def count_sore_losers(self, target, undead) -> None:
        boost = 0
        for c in undead.army.cards:
            if isinstance(c, SoreLoser) and not c is self:
                boost += self.army.player.level
                if c.triplet:
                    boost += self.army.player.level
        if MinionClass.Undead in undead.classes:
            undead.sore_loser_boost = boost
                
    def put_hook_existing(self) -> None:
        self.army.hooks["on_minion_play"].append(self.put_hook_new)
        for m in self.army.cards:
            if MinionClass.Undead in m.classes:
                m.hooks["on_attack_pre"].append(partial(self.count_sore_losers, undead=m))
                m.hooks["on_defence_pre"].append(partial(self.count_sore_losers, undead=m))

    def put_hook_new(self, played) -> None:
        if MinionClass.Undead in played.classes:
            played.hooks["on_attack_pre"].append(partial(self.count_sore_losers, undead=played))
            played.hooks["on_defence_pre"].append(partial(self.count_sore_losers, undead=played))

    def decrease_boost(self) -> None:
        for m in self.army.cards:
            if MinionClass.Undead in m.classes:
                m.sore_loser_boost -= 2
                if self.triplet:
                    m.sore_loser_boost -= 2

    def reset_boost(self) -> None:
        for m in self.army.cards:
            if MinionClass.Undead in m.classes:
                m.sore_loser_boost = 0
