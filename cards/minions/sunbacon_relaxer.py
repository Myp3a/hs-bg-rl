from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.blood_gem import BloodGem

if TYPE_CHECKING:
    from models.army import Army


class SunBaconRelaxer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 21
        self.classes = [MinionClass.Quilboar]
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 2
        self.hooks["on_sell"].append(self.give_blood_gem)

    def give_blood_gem(self) -> None:
        count = 2
        if self.triplet:
            count = 4
        self.log.debug(f"{self} giving {count} blood gems to {self.army.player}")
        for _ in range(count):
            self.army.player.hand.add(BloodGem(self.army.player), len(self.army.player.hand))