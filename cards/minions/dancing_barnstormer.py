from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class DancingBarnstormer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 32
        self.classes = [MinionClass.Elemental]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 1
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["deathrattle"].append(self.boost_elementals)

    def boost_elementals(self) -> None:
        self.army.player.tavern_elemental_boost += 1
        if self.triplet:
            self.army.player.tavern_elemental_boost += 1
