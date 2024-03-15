from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class CultistSthara(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 183
        self.classes = []
        self.level = 6
        self.base_attack_value = 11
        self.base_health_value = 3
        self.base_stealth = True
        self.hooks["deathrattle"].append(self.summon_demon)

    def summon_demon(self, position):
        died_demons = [d for d in self.army.dead]
        if not died_demons:
            return
        demon = died_demons[0]
        demon.attack_temp_boost = 0
        demon.health_temp_boost = 0
        self.army.add(demon, position)
