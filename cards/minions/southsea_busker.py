from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SouthseaBusker(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 20
        self.classes = [MinionClass.Pirate]
        self.level = 1
        self.base_attack_value = 3
        self.base_health_value = 1
        self.hooks["on_turn_start"].append(self.give_gold)
        self.gave_gold = False

    def give_gold(self) -> None:
        if not self.gave_gold:
            self.log.debug(f"{self} giving gold")
            self.gave_gold = True
            self.army.player.gold += 1
            if self.triplet:
                self.army.player.gold += 1