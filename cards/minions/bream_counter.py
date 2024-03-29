from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class BreamCounter(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 102
        self.classes = [MinionClass.Murloc]
        self.level = 4
        self.base_attack_value = 5
        self.base_health_value = 5
        self.hooks["on_get"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_play")
        self.army.hooks["on_minion_play"].append(self.boost_values)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_play")
        self.army.hooks["on_minion_play"].remove(self.boost_values)

    def boost_values(self, played):
        if MinionClass.Murloc in played.classes and self in self.army.player.hand.cards:
            self.log.debug(f"{self} boosting values because murloc was played")
            if self.triplet:
                atk_boost = 6
                hlt_boost = 6
            else:
                atk_boost = 3
                hlt_boost = 3
            self.attack_perm_boost += atk_boost
            self.health_perm_boost += hlt_boost
