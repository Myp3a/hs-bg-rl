from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .sky_pirate import SkyPirate

if TYPE_CHECKING:
    from models.army import Army


class Scallywag(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 15
        self.classes = [MinionClass.Pirate]
        self.level = 1
        self.base_attack_value = 3
        self.base_health_value = 1
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["deathrattle"].append(self.summon_sky_pirate)

    def summon_sky_pirate(self, position) -> None:
        pirate = SkyPirate(self.army)
        if self.triplet:
            pirate.triplet = True
            pirate.base_attack_value *= 2
            pirate.base_health_value *= 2
            pirate.attack_value = pirate.base_attack_value
            pirate.health_value = pirate.base_health_value
        self.army.add(pirate, position)
