from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class KalecgosArcaneAspect(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 195
        self.classes = [MinionClass.Dragon]
        self.level = 6
        self.base_attack_value = 2
        self.base_health_value = 10
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_battlecry"].append(self.boost_dragons)

    def remove_hook(self) -> None:
        self.army.hooks["on_battlecry"].remove(self.boost_dragons)

    def boost_dragons(self, cried) -> None:
        targets = [d for d in self.army.cards if MinionClass.Dragon in d.classes]
        if not targets:
            return
        for t in targets:
            if self.triplet:
                atk_boost = 2
                hlt_boost = 2
            else:
                atk_boost = 1
                hlt_boost = 1
            t.attack_perm_boost += atk_boost
            t.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(t, atk_boost, hlt_boost)
