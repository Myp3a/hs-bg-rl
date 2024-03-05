from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class UtilityDrone(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 136
        self.classes = [MinionClass.Mech]
        self.level = 1
        self.base_attack_value = 3
        self.base_health_value = 4
        self.hooks["on_turn_end"].append(self.boost_magnited)

    def boost_magnited(self):
        targets = [t for t in self.army.cards if len(t.magnited) > 0]
        for t in targets:
            if self.triplet:
                atk_boost = 2
                hlt_boost = 2
            else:
                atk_boost = 1
                hlt_boost = 1
            for _ in t.magnited:
                t.attack_perm_boost += atk_boost
                t.health_perm_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(t, atk_boost, hlt_boost)
