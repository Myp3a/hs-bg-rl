from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion

if TYPE_CHECKING:
    from models.army import Army


class Yrel(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 59
        self.classes = []
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 3
        self.hooks["on_attack_post"].append(self.boost_army)

    def boost_army(self, attack_target) -> None:
        diff_classes = set()
        for card in self.army.cards:
            diff_classes |= set(card.classes)
        self.log.debug(f"{self} found {len(diff_classes)} diff classes")
        for single_class in diff_classes:
            target = random.choice([c for c in self.army.cards if single_class in c.classes])
            self.log.debug(f"{self} boosting {target}")
            if self.triplet:
                atk_boost = 2
                hlt_boost = 4
            else:
                atk_boost = 1
                hlt_boost = 2
            target.attack_temp_boost += atk_boost
            target.health_temp_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_temp"]:
                hook(target, atk_boost, hlt_boost)
