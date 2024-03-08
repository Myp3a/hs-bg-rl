from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class HungrySnapjaw(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 38
        self.classes = [MinionClass.Beast]
        self.level = 2
        self.base_attack_value = 5
        self.base_health_value = 2
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_minion_play"].append(self.boost_health)

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_play"].remove(self.boost_health)
        
    def boost_health(self, played) -> None:
        if MinionClass.Beast in played.classes:
            if self.triplet:
                hlt_boost = 2
            else:
                hlt_boost = 1
            self.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(self, 0, hlt_boost)
