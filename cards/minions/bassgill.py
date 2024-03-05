from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Bassgill(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 99
        self.classes = [MinionClass.Murloc]
        self.level = 4
        self.base_attack_value = 7
        self.base_health_value = 2
        self.hooks["deathrattle"].append(self.summon_from_hand)

    def choose_and_summon(self, position):
        if len(self.army) == 7:
            return
        to_summon = [t for t in self.army.player.hand if isinstance(t, Minion) and not t.summoned and MinionClass.Murloc in t.classes]
        if len(to_summon) == 0:
            return
        summon = sorted(to_summon, key=lambda summ: summ.health_value, reverse=True)[0]
        self.army.add(summon, position)
        for hook in self.army.hooks["on_minion_summon"]:
            hook(summon)

    def summon_from_hand(self, position) -> None:
        if self.triplet:
            self.choose_and_summon(position)
        self.choose_and_summon(position)
