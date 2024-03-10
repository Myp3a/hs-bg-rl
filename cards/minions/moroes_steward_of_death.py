from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MoroesStewardOfDeath(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 164
        self.classes = [MinionClass.Undead]
        self.level = 5
        self.base_attack_value = 6
        self.base_health_value = 6
        self.base_rebirth = True
        self.hooks["deathrattle"].append(self.boost_undead)

    def boost_undead(self, position) -> None:
        for c in self.army.cards:
            if MinionClass.Undead in c.classes:
                if self.triplet:
                    atk_boost = 2
                    hlt_boost = 10
                else:
                    atk_boost = 1
                    hlt_boost = 5
                c.attack_temp_boost += atk_boost
                c.health_temp_boost += hlt_boost
