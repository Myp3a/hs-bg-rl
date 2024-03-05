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
        self.army.player.blood_gem_attack += 1
        if self.triplet:
            self.army.player.blood_gem_attack += 1
