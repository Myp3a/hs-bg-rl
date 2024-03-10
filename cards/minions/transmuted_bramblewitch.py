from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class TransmutedBramblewitch(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 176
        self.classes = [MinionClass.Elemental, MinionClass.Quilboar]
        self.level = 5
        self.base_attack_value = 4
        self.base_health_value = 4
        self.changes_left = 0
        self.hooks["on_attack_pre"].append(self.change_values)
        self.hooks["on_turn_start"].append(self.reset_changes)
        self.hooks["on_play"].append(self.reset_changes)

    def reset_changes(self):
        if self.triplet:
            self.changes_left = 2
        else:
            self.changes_left = 1

    def change_values(self, defender: Minion) -> None:
        if self.changes_left > 0:
            self.changes_left -= 1
            defender.attack_temp_boost -= defender.attack_value - 3
            defender.health_temp_boost -= defender.health_value - 3
