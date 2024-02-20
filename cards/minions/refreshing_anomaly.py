from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RefreshingAnomaly(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 12
        self.classes = [MinionClass.Elemental]
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 4
        self.hooks["battlecry"].append(self.give_free_roll)

    def give_free_roll(self) -> None:
        self.army.player.free_rolls += 1
        if self.triplet:
            self.army.player.free_rolls += 1
