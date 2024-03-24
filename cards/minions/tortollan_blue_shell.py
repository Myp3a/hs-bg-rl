from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class TortollanBlueShell(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 175
        self.classes = []
        self.level = 5
        self.base_attack_value = 4
        self.base_health_value = 7
        self.hooks["on_sell"].append(self.give_gold)

    def give_gold(self):
        if self.army.player.lost_last_turn:
            self.log.debug(f"{self} giving additional gold")
            self.army.player.gold += 4
