from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class LavaLurker(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 40
        self.classes = [MinionClass.Naga]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 5
        self.first_change = True
        self.hooks["on_temp_values_change"].append(self.permanent_bonus)
        self.hooks["on_turn_start"].append(self.reset_first)
        
    def reset_first(self) -> None:
        self.first_change = True

    def permanent_bonus(self) -> None:
        self.attack_perm_boost += self.attack_temp_boost
        self.health_perm_boost += self.health_temp_boost
        self.attack_temp_boost = 0
        self.health_temp_boost = 0
        self.first_change = False
