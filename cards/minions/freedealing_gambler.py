from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class FreedealingGambler(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 35
        self.classes = [MinionClass.Pirate]
        self.level = 2
        self.base_attack_value = 3
        self.base_health_value = 3
        self.hooks["on_sell"].append(self.give_gold)

    def give_gold(self) -> None:
        self.log.debug(f"{self} giving additional gold")
        if self.triplet:
            self.army.player.gold += 3
        self.army.player.gold += 2
