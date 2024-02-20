from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class BronzeSandspewer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 29
        self.classes = [MinionClass.Dragon]
        self.level = 2
        self.base_attack_value = 1
        self.base_health_value = 1
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["on_turn_end"].append(self.boost_values)

    def boost_values(self) -> None:
        if len(self.army) == 7:
            self.attack_value += 1
            self.health_value += 1
            if self.triplet:
                self.attack_value += 1
                self.health_value += 1