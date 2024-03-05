from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class StrongshellScavenger(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 132
        self.classes = []
        self.level = 4
        self.base_attack_value = 2
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.boost_taunt_minions)

    def boost_taunt_minions(self):
        targets = [t for t in self.army.cards if not t is self and t.taunt]
        for t in targets:
            if self.triplet:
                atk_boost = 4
                hlt_boost = 4
            else:
                atk_boost = 2
                hlt_boost = 2
            t.attack_perm_boost += atk_boost
            t.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(t, atk_boost, hlt_boost)
