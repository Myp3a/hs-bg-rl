from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MicroMummy(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.classes = [MinionClass.Mech, MinionClass.Undead]
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 2
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["on_turn_end"].append(self.boost_attack)

    def boost_attack(self) -> None:
        available_targets = [c for c in self.army.cards if not self]
        if len(available_targets) == 0:
            return
        target = random.choice(available_targets)
        target.attack_value += 1
        if self.triplet:
            target.attack_value += 1