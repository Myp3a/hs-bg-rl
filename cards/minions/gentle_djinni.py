from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class GentleDjinni(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 152
        self.classes = [MinionClass.Elemental]
        self.level = 5
        self.base_attack_value = 4
        self.base_health_value = 5
        self.hooks["deathrattle"].append(self.summon_and_get_elemental)

    def select_and_get_elemental(self, position):
        elementals = [e for e in self.army.player.tavern.available_cards() if e.level <= self.army.player.level and MinionClass.Elemental in e.classes]
        if not elementals:
            self.log.debug(f"{self} found no elemental to summon")
            return
        elemental = random.choice(elementals)
        self.log.debug(f"{self} getting {elemental} from tavern and spawning it")
        self.army.player.tavern.buy(elemental)
        elemental.army = self.army
        for hook in elemental.hooks["on_get"]:
            hook()
        self.army.player.hand.add(elemental, len(self.army.player.hand.cards))
        self.army.add(elemental, position)

    def summon_and_get_elemental(self, position):
        if self.triplet:
            self.select_and_get_elemental(position)
        self.select_and_get_elemental(position)
