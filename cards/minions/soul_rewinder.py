from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SoulRewinder(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 53
        self.classes = [MinionClass.Demon]
        self.level = 2
        self.base_attack_value = 3
        self.base_health_value = 1
        self.army.hooks["on_hero_damage"].append(self.rewind_damage)

    def rewind_damage(self, damage) -> None:
        self.army.player.health += damage
        if self.triplet:
            hlt_boost = 2
        else:
            hlt_boost = 1
        self.health_perm_boost += 1
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(self, 0, hlt_boost)
