from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SteadfastSpirit(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 131
        self.classes = [MinionClass.Undead]
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 1
        self.base_rebirth = True
        self.hooks["deathrattle"].append(self.boost_minions)

    def boost_minions(self, position):
        targets = [t for t in self.army.cards if not t is self]
        for t in targets:
            if self.triplet:
                atk_boost = 2
                hlt_boost = 2
            else:
                atk_boost = 1
                hlt_boost = 1
            if self.in_fight:
                t.attack_temp_boost += atk_boost
                t.health_temp_boost += hlt_boost
            else:
                t.attack_perm_boost += atk_boost
                t.health_perm_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(t, atk_boost, hlt_boost)
