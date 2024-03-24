from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class CorruptedMyrmidon(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 147
        self.classes = [MinionClass.Naga]
        self.level = 5
        self.base_attack_value = 3
        self.base_health_value = 3
        self.hooks["on_fight_start"].append(self.boost_stats)

    def boost_stats(self) -> None:
        if self.triplet:
            atk_bonus = self.attack_value * 2
            hlt_bonus = self.health_value * 2
        else:
            atk_bonus = self.attack_value
            hlt_bonus = self.health_value
        self.log.debug(f"{self} getting bonus {atk_bonus}/{hlt_bonus}")
        self.attack_temp_boost += atk_bonus
        self.health_temp_boost += hlt_bonus
