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
        if self.magnited_to is None:
            self.attack_perm_boost += 1
            self.health_perm_boost += 1
            if self.triplet:
                self.attack_perm_boost += 1
                self.health_perm_boost += 1
        else:
            self.magnited_to.attack_perm_boost += 1
            self.magnited_to.health_perm_boost += 1
            if self.triplet:
                self.magnited_to.attack_perm_boost += 1
                self.magnited_to.health_perm_boost += 1
