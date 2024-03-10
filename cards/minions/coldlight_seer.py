from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class ColdlightSeer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 31
        self.classes = [MinionClass.Murloc]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.boost_murloc)

    def boost_murloc(self) -> None:
        for minion in self.army.cards:
            if MinionClass.Murloc in minion.classes:
                if not minion is self:
                    if self.triplet:
                        hlt_boost = 4
                    else:
                        hlt_boost = 2
                    if self.in_fight:
                        minion.health_temp_boost += hlt_boost
                    else:
                        minion.health_perm_boost += hlt_boost
                        for hook in self.army.hooks["on_values_change_perm"]:
                            hook(minion, 0, hlt_boost)