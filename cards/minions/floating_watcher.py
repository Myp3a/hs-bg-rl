from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class FloatingWatcher(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 107
        self.classes = [MinionClass.Demon]
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 4
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_sell"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_hero_damage")
        self.army.hooks["on_hero_damage"].append(self.boost_values)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_hero_damage")
        self.army.hooks["on_hero_damage"].remove(self.boost_values)

    def boost_values(self, damage) -> None:
        self.log.debug(f"{self} found hero damage, boosting self")
        if self.triplet:
            atk_boost = 4
            hlt_boost = 4
        else:
            atk_boost = 2
            hlt_boost = 2
        self.attack_perm_boost += atk_boost
        self.health_perm_boost += hlt_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(self, atk_boost, hlt_boost)
