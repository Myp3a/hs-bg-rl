from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MicroMummy(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 9
        self.classes = [MinionClass.Mech, MinionClass.Undead]
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 2
        self.hooks["on_turn_end"].append(self.boost_attack)

    def boost_attack(self) -> None:
        available_targets = [c for c in self.army.cards if not self]
        if len(available_targets) == 0:
            return
        target = random.choice(available_targets)
        if self.triplet:
            atk_boost = 2
        else:
            atk_boost = 1
        target.attack_perm_boost += atk_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(target, atk_boost, 0)