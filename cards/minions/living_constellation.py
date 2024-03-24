from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class LivingConstellation(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 76
        self.classes = []
        self.level = 3
        self.base_attack_value = 4
        self.base_health_value = 2
        self.hooks["battlecry"].append(self.boost_minion)

    def boost_minion(self):
        # TODO: make targeted battlecry mechanic
        diff_classes = set()
        for card in self.army.cards:
            diff_classes |= set(card.classes)
        if self.triplet:
            atk_boost = 2
            hlt_boost = 2
        else:
            atk_boost = 1
            hlt_boost = 1
        atk_boost *= len(diff_classes)
        hlt_boost *= len(diff_classes)
        self.log.debug(f"{self} found {len(diff_classes)} different classes")
        targets = [t for t in self.army.cards if not t is self]
        if not targets:
            self.log.debug(f"{self} found no targets to boost")
            return
        target = random.choice(targets)
        self.log.debug(f"{self} boosting {target}")
        if self.in_fight:
            target.attack_temp_boost += atk_boost
            target.health_temp_boost += hlt_boost
        else:
            target.attack_perm_boost += atk_boost
            target.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(target, atk_boost, hlt_boost)
