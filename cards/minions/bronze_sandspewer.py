from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class BronzeSandspewer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 29
        self.classes = [MinionClass.Dragon]
        self.level = 2
        self.base_attack_value = 1
        self.base_health_value = 1
        self.hooks["on_turn_end"].append(self.boost_values)

    def boost_values(self) -> None:
        if len(self.army) == 7:
            self.log.debug(f"{self} found 7 minions, boosting self")
            if self.triplet:
                atk_boost = 2
                hlt_boost = 2
            else:
                atk_boost = 1
                hlt_boost = 1
            self.attack_perm_boost += atk_boost
            self.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(self, atk_boost, hlt_boost)
