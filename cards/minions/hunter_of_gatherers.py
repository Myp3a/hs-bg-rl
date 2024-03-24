from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class HunterOfGatherers(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 155
        self.classes = [MinionClass.Dragon]
        self.level = 5
        self.base_attack_value = 3
        self.base_health_value = 6
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_values_change")
        self.army.hooks["on_values_change_perm"].append(self.boost_health)
        self.army.hooks["on_values_change_temp"].append(self.boost_health)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_values_change")
        self.army.hooks["on_values_change_perm"].remove(self.boost_health)
        self.army.hooks["on_values_change_temp"].remove(self.boost_health)

    def boost_health(self, target, atk_boost, hlt_boost) -> None:
        if self.health_value > 0 and atk_boost > 0 and target is self:
            self.log.debug(f"{self} boosting army health")
            if self.triplet:
                hlt_boost = 2
            else:
                hlt_boost = 1
            for c in self.army.cards:
                if self.in_fight:
                    c.health_temp_boost += hlt_boost
                else:
                    c.health_perm_boost += hlt_boost
                    for hook in self.army.hooks["on_values_change_perm"]:
                        hook(c, 0, hlt_boost)
