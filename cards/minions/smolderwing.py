from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Smolderwing(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 119
        self.classes = [MinionClass.Dragon]
        self.level = 1
        self.base_attack_value = 2
        self.base_health_value = 1
        self.hooks["battlecry"].append(self.boost_dragon)

    def boost_dragon(self):
        targets = [t for t in self.army.cards if MinionClass.Dragon in t.classes and not t is self]
        if not targets:
            self.log.debug(f"{self} found no targets")
            return
        target = random.choice(targets)
        self.log.debug(f"{self} boosting {target}")
        if self.triplet:
            atk_boost = 10
        else:
            atk_boost = 5
        target.attack_perm_boost += atk_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(target, atk_boost, 0)
