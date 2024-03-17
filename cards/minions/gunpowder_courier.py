from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class GunpowderCourier(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 72
        self.classes = [MinionClass.Pirate]
        self.level = 3
        self.base_attack_value = 2
        self.base_health_value = 6
        self.gold_left = 5
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_gold_spent"].append(self.boost_pirates)
        
    def remove_hook(self) -> None:
        self.gold_left = 5
        self.army.hooks["on_gold_spent"].remove(self.boost_pirates)

    def boost_pirates(self, spent_amount):
        self.gold_left -= spent_amount
        if self.gold_left <= 0:
            if self.triplet:
                atk_boost = 2
            else:
                atk_boost = 1
            pirates = [c for c in self.army.cards if MinionClass.Pirate in c.classes]
            for p in pirates:
                p.attack_perm_boost += atk_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(p, atk_boost, 0)
            self.gold_left += 5
