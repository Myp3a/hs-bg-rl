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
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["on_turn_start"].append(self.decrease_attack)

    def decrease_attack(self) -> None:
        self.attack_value -= 1