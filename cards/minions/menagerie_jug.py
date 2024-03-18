from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MenagerieJug(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 116
        self.classes = []
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.boost_minions)

    def boost_minions(self):
        diff_classes = set()
        for card in self.army.cards:
            diff_classes |= set(card.classes)
        if len(diff_classes) > 3:
            target_classes = random.sample(list(diff_classes), k=3)
        else:
            target_classes = list(diff_classes)
        for single_class in target_classes:
            target = random.choice([c for c in self.army.cards if single_class in c.classes])
            if self.triplet:
                atk_boost = 4
                hlt_boost = 4
            else:
                atk_boost = 2
                hlt_boost = 2
            if self.in_fight:
                target.attack_temp_boost += atk_boost
                target.health_temp_boost += hlt_boost
            else:
                target.attack_perm_boost += atk_boost
                target.health_perm_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(target, atk_boost, hlt_boost)
