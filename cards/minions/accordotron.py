from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class AccordOTron(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 60
        self.classes = [MinionClass.Mech]
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 3
        self.hooks["on_turn_start"].append(self.give_gold)

    def give_gold(self) -> None:
        if self.triplet:
            self.army.player.gold += 1
        self.army.player.gold += 1