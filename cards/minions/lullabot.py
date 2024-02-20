from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Lullabot(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 41
        self.classes = [MinionClass.Mech]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 2
        self.magnetic = True
        self.hooks["on_turn_end"].append(self.boost_values)
        
    def boost_values(self) -> None:
        if self.triplet:
            atk_boost = 2
            hlt_boost = 2
        else:
            atk_boost = 1
            hlt_boost = 1
        if self.magnited_to is None:
            target = self
        else:
            target = self.magnited_to
        target.attack_perm_boost += atk_boost
        target.health_perm_boost += hlt_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(target, atk_boost, hlt_boost)
