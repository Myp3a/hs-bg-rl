from __future__ import annotations
from typing import TYPE_CHECKING
import random

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Ghastcoiler(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 191
        self.classes = [MinionClass.Beast]
        self.level = 6
        self.base_attack_value = 7
        self.base_health_value = 7
        self.hooks["deathrattle"].append(self.summon_deathrattle)

    def summon_deathrattle(self, position):
        if self.triplet:
            count = 4
        else:
            count = 2
        for _ in range(count):
            self.select_and_summon_deathrattle(position)

    def select_and_summon_deathrattle(self, position) -> None:
        dr = [d for d in self.army.player.tavern.cards if d.hooks["deathrattle"]]
        if not dr:
            return
        minion = random.choice(dr)
        new_minion = type(minion)(self.army)
        for hook in new_minion.hooks["on_get"]:
            hook()
        new_minion.base_attack_value = 7
        new_minion.base_health_value = 7
        if len(self.army) == 7:
            return
        self.army.add(new_minion, position)
        for hook in self.army.hooks["on_minion_summon"]:
            hook(new_minion)
