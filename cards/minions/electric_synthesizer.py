from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class ElectricSynthesizer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 68
        self.classes = [MinionClass.Dragon]
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 4
        self.hooks["battlecry"].append(self.boost_dragons)

    def boost_dragons(self) -> None:
        if self.triplet:
            atk_boost = 4
            hlt_boost = 2
        else:
            atk_boost = 2
            hlt_boost = 1
        targets = [t for t in self.army.cards if not t is self and MinionClass.Dragon in t.classes]
        if len(targets) == 0:
            return
        for t in targets:
            t.attack_perm_boost += atk_boost
            t.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(t, atk_boost, hlt_boost)
