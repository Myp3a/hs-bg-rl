from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class NerubianDeathswarmer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 45
        self.classes = [MinionClass.Undead]
        self.level = 2
        self.base_attack_value = 1
        self.base_health_value = 4
        self.hooks["battlecry"].append(self.boost_undead_attack)

    def boost_undead_attack(self) -> None:
        if self.triplet:
            atk_boost = 2
        else:
            atk_boost = 1
        self.army.player.undead_attack_boost += atk_boost
        for c in self.army.cards:
            if MinionClass.Undead in c.classes:
                if self.in_fight:
                    c.attack_temp_boost += 1
                else:
                    c.attack_perm_boost += atk_boost
                    for hook in self.army.hooks["on_values_change_perm"]:
                        hook(c, atk_boost, 0)
