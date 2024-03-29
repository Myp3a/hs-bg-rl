from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.blood_gem import BloodGem

if TYPE_CHECKING:
    from models.army import Army


class RazorfenGeomancer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 11
        self.classes = [MinionClass.Quilboar]
        self.level = 1
        self.base_attack_value = 3
        self.base_health_value = 1
        self.hooks["battlecry"].append(self.give_blood_gem)

    def give_blood_gem(self) -> None:
        self.log.debug(f"{self} giving blood gem to {self.army.player}")
        self.army.player.hand.add(BloodGem(self.army.player), len(self.army.player.hand))
        if self.triplet:
            self.army.player.hand.add(BloodGem(self.army.player), len(self.army.player.hand))