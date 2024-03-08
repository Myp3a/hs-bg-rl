from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class WhelpSmuggler(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 58
        self.classes = []
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 3
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_values_change_perm"].append(self.boost_dragon)
        self.army.hooks["on_values_change_temp"].append(self.boost_dragon_temp)

    def remove_hook(self) -> None:
        self.army.hooks["on_values_change_perm"].remove(self.boost_dragon)
        self.army.hooks["on_values_change_temp"].remove(self.boost_dragon_temp)

    def boost_dragon(self, target: Minion, attack_boost, health_boost) -> None:
        if MinionClass.Dragon in target.classes:
            if attack_boost > 0:
                if self.triplet:
                    hlt_boost = 2
                else:
                    hlt_boost = 1
                target.health_perm_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(target, 0, hlt_boost)

    def boost_dragon_temp(self, target: Minion, attack_boost, health_boost) -> None:
        if MinionClass.Dragon in target.classes:
            if attack_boost > 0:
                if self.triplet:
                    hlt_boost = 2
                else:
                    hlt_boost = 1
                target.health_temp_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_temp"]:
                    hook(self, 0, hlt_boost)