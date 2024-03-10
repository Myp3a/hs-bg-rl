from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MasterOfRealities(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 160
        self.classes = []
        self.level = 5
        self.base_attack_value = 6
        self.base_health_value = 6
        self.base_taunt = True
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_values_change_perm"].append(self.boost_values)
        self.army.hooks["on_values_change_temp"].append(self.boost_values)

    def remove_hook(self) -> None:
        self.army.hooks["on_values_change_perm"].remove(self.boost_values)
        self.army.hooks["on_values_change_temp"].remove(self.boost_values)

    def boost_values(self, target, atk_boost, hlt_boost):
        if MinionClass.Elemental in target.classes:
            if self.triplet:
                atk_boost = 2
                hlt_boost = 2
            else:
                atk_boost = 1
                hlt_boost = 1
            if self.in_fight:
                self.attack_temp_boost += atk_boost
                self.health_temp_boost += hlt_boost
            else:
                self.attack_perm_boost += atk_boost
                self.health_perm_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(self, atk_boost, hlt_boost)
