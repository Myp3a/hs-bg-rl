from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class TheWalkingFort(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 205
        self.classes = []
        self.level = 6
        self.base_attack_value = 4
        self.base_health_value = 6
        self.hooks["on_turn_end"].append(self.boost_taunt)
    
    def boost_taunt(self):
        targets = [t for t in self.army.cards if t.taunt]
        if not targets:
            return
        targets = random.sample(targets, k=min(len(targets), 4))
        for t in targets:
            if self.triplet:
                atk_boost = 8
                hlt_boost = 8
            else:
                atk_boost = 4
                hlt_boost = 4
            t.attack_perm_boost += atk_boost
            t.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(t, atk_boost, hlt_boost)
