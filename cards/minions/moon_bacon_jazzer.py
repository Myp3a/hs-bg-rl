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
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.boost_blood_gem_health)

    def boost_blood_gem_health(self) -> None:
        self.army.player.blood_gem_health += 1
        if self.triplet:
            self.army.player.blood_gem_health += 1
