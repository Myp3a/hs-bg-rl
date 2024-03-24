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
        self.hooks["deathrattle"].append(self.boost_elementals)

    def boost_elementals(self, position) -> None:
        if self.triplet:
            el_boost = 2
        else:
            el_boost = 1
        self.log.debug(f"{self} boosting elementals by {el_boost}")
        self.army.player.tavern_elemental_boost += el_boost
