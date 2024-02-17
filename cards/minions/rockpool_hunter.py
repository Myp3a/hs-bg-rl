from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RockpoolHunter(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 14
        self.classes = [MinionClass.Mech, MinionClass.Undead]
        self.level = 1
        self.base_attack_value = 2
        self.base_health_value = 3
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["battlecry"].append(self.boost_murloc_values)

    def boost_murloc_values(self) -> None:
        available_targets = [c for c in self.army.cards if not self and MinionClass.Murloc in c.classes]
        if len(available_targets) == 0:
            return
        target = random.choice(available_targets)
        target.attack_value += 1
        target.health_value += 1
        if self.triplet:
            target.attack_value += 1
            target.health_value += 1