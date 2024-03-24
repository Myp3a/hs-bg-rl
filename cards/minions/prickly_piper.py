from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class PricklyPiper(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 85
        self.classes = [MinionClass.Quilboar]
        self.level = 3
        self.base_attack_value = 5
        self.base_health_value = 1
        self.hooks["deathrattle"].append(self.boost_blood_gem_attack)

    def boost_blood_gem_attack(self, position) -> None:
        if self.triplet:
            atk_boost = 2
        else:
            atk_boost = 1
        self.log.debug(f"{self} boosting blood gem attack by {atk_boost}")
        self.army.player.blood_gem_attack += atk_boost
