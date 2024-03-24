from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MoonBaconJazzer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 43
        self.classes = [MinionClass.Quilboar]
        self.level = 3
        self.base_attack_value = 2
        self.base_health_value = 5
        self.hooks["battlecry"].append(self.boost_blood_gem_health)

    def boost_blood_gem_health(self) -> None:
        if self.triplet:
            hlt_boost = 2
        else:
            hlt_boost = 1
        self.log.debug(f"{self} boosting blood gem health by {hlt_boost}")
        self.army.player.blood_gem_health += hlt_boost
