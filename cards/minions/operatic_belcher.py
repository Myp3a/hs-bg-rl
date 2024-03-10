from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class OperaticBelcher(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 166
        self.classes = [MinionClass.Murloc]
        self.level = 5
        self.base_attack_value = 5
        self.base_health_value = 2
        self.base_toxic = True
        self.hooks["deathrattle"].append(self.give_toxic)

    def choose_and_give_toxic(self):
        targets = [t for t in self.army.cards if MinionClass.Murloc in t.classes and not t.toxic]
        if len(targets) == 0:
            return
        target = random.choice(targets)
        target.feature_overrides["toxic"].append({"state": True, "one_turn": self.in_fight})

    def give_toxic(self, position):
        if self.triplet:
            self.choose_and_give_toxic()
        self.choose_and_give_toxic()
