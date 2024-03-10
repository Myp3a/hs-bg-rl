from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class KingBagurgle(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 158
        self.classes = [MinionClass.Murloc]
        self.level = 5
        self.base_attack_value = 6
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.boost_murloc)

    def boost_murloc(self, position) -> None:
        for c in self.army.cards:
            if MinionClass.Murloc in c.classes:
                if self.triplet:
                    atk_boost = 6
                    hlt_boost = 6
                else:
                    atk_boost = 3
                    hlt_boost = 3
                c.attack_perm_boost += atk_boost
                c.health_perm_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(c, atk_boost, hlt_boost)
