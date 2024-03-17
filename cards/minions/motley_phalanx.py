from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MotleyPhalanx(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 197
        self.classes = [c.value for c in MinionClass]
        self.level = 6
        self.base_attack_value = 4
        self.base_health_value = 4
        self.hooks["deathrattle"].append(self.boost_minions)
        
    def boost_minions(self):
        diff_classes = set()
        for card in self.army.cards:
            diff_classes |= set(card.classes)
        for single_class in diff_classes:
            target = random.choice([c for c in self.army.cards if single_class in c.classes])
            if self.triplet:
                atk_boost = 8
                hlt_boost = 8
            else:
                atk_boost = 4
                hlt_boost = 4
            if self.in_fight:
                target.attack_temp_boost += atk_boost
                target.health_temp_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_temp"]:
                    hook(target, atk_boost, hlt_boost)
            else:
                target.attack_perm_boost += atk_boost
                target.health_perm_boost += hlt_boost
