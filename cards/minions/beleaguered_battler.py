from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion

if TYPE_CHECKING:
    from models.army import Army


class BeleagueredBattler(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 1
        self.classes = []
        self.level = 1
        self.base_attack_value = 4
        self.base_health_value = 5
        self.hooks["on_play"].append(self.reset_attack_drop)
        self.hooks["on_turn_start"].append(self.decrease_attack)

    def decrease_attack(self) -> None:
        atk_boost = -1
        if self.attack_value > 0:
            self.attack_perm_boost += atk_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(self, atk_boost, 0)

    def reset_attack_drop(self) -> None:
        self.attack_perm_boost = 0