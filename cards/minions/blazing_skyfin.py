from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class BlazingSkyfin(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 27
        self.classes = [MinionClass.Murloc, MinionClass.Dragon]
        self.level = 2
        self.base_attack_value = 1
        self.base_health_value = 3
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_minion_play"].append(self.boost_values)

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_play"].remove(self.boost_values)

    def boost_values(self, played: Minion) -> None:
        if len(played.hooks["battlecry"]) > 0:
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