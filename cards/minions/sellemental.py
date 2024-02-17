from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .water_droplet import WaterDroplet

if TYPE_CHECKING:
    from models.army import Army


class Sellemental(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 17
        self.classes = [MinionClass.Elemental]
        self.level = 1
        self.base_attack_value = 2
        self.base_health_value = 2
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["on_sell"].append(self.give_water_droplet)

    def give_water_droplet(self) -> None:
        drop = WaterDroplet(self.army)
        if self.triplet:
            drop.triplet = True
            drop.base_attack_value *= 2
            drop.base_health_value *= 2
            drop.attack_value = drop.base_attack_value
            drop.health_value = drop.base_health_value
        self.army.player.hand.add(drop, len(self.army.player.hand))