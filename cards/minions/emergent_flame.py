from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class EmergentFlame(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 106
        self.classes = []
        self.level = 4
        self.base_attack_value = 5
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.boost_elemental)

    def boost_elemental(self) -> None:
        targets = [t for t in self.army.cards if MinionClass.Elemental in t.classes and not t is self]
        if len(targets) == 0:
            return
        target = random.choice(targets)
        if self.triplet:
            atk_boost = (self.army.player.rolls_on_turn + 1) * 2
            hlt_boost = (self.army.player.rolls_on_turn + 1) * 2
        else:
            atk_boost = self.army.player.rolls_on_turn + 1
            hlt_boost = self.army.player.rolls_on_turn + 1
        target.attack_perm_boost += atk_boost
        target.health_perm_boost += hlt_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(target, atk_boost, hlt_boost)
