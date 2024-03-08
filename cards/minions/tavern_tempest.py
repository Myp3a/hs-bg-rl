from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class TavernTempest(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 133
        self.classes = [MinionClass.Elemental]
        self.level = 4
        self.base_attack_value = 2
        self.base_health_value = 2
        self.hooks["battlecry"].append(self.get_elemental)

    def select_and_get_elemental(self):
        elementals = [e for e in self.army.player.tavern.available_cards() if e.level <= self.army.player.level]
        if len(elementals) == 0:
            return
        if len(self.army.player.hand.cards) == 10:
            return
        elemental = random.choice(elementals)
        self.army.player.tavern.buy(elemental)
        elemental.army = self.army
        for hook in elemental.hooks["on_get"]:
            hook()
        self.army.player.hand.add(elemental, len(self.army.player.hand.cards))

    def get_elemental(self):
        if self.triplet:
            self.select_and_get_elemental()
        self.select_and_get_elemental()
