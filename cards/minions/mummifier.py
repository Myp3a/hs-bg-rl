from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Mummifier(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 79
        self.classes = [MinionClass.Undead]
        self.level = 3
        self.base_attack_value = 5
        self.base_health_value = 2
        self.hooks["deathrattle"].append(self.give_rebirth)

    def choose_and_give_rebirth(self):
        targets = [t for t in self.army.cards if MinionClass.Undead in t.classes and not t.rebirth]
        if not targets:
            self.log.debug(f"{self} found no targets")
            return
        target = random.choice(targets)
        self.log.debug(f"{self} giving rebirth to {target}")
        target.feature_overrides["rebirth"].append({"state": True, "one_turn": self.in_fight})
        target.reborn = False

    def give_rebirth(self, position):
        if self.triplet:
            self.choose_and_give_rebirth()
        self.choose_and_give_rebirth()
