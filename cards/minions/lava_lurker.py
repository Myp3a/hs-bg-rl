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
        self.saved_changes = 2
        self.hooks["on_turn_start"].append(self.reset_first)
        self.hooks["on_turn_start"].append(self.put_hook)
        self.hooks["on_turn_end"].append(self.remove_hook)
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.try_remove_hook)
        
    def put_hook(self) -> None:
        self.hooks["on_temp_values_change"].append(self.permanent_bonus)

    def remove_hook(self) -> None:
        self.hooks["on_temp_values_change"].remove(self.permanent_bonus)

    def try_remove_hook(self) -> None:
        try:
            self.remove_hook()
        except:
            pass

    def reset_first(self) -> None:
        if self.triplet:
            self.saved_changes = 2
        else:
            self.saved_changes = 1

    def permanent_bonus(self) -> None:
        if self.saved_changes > 0:
            self.saved_changes -= 1
            self.attack_perm_boost += self.attack_temp_boost
            self.health_perm_boost += self.health_temp_boost
            self.attack_temp_boost = 0
            self.health_temp_boost = 0
