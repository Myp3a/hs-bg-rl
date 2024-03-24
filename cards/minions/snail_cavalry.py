from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SnailCavalry(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 52
        self.classes = [MinionClass.Naga]
        self.level = 2
        self.base_attack_value = 5
        self.base_health_value = 2
        self.first_cast = True
        self.hooks["on_turn_start"].append(self.reset_first_cast)
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_spell_cast")
        self.army.hooks["on_spell_cast"].append(self.boost_health)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_spell_cast")
        self.army.hooks["on_spell_cast"].remove(self.boost_health)

    def reset_first_cast(self) -> None:
        self.first_cast = True

    def boost_health(self, casted, target) -> None:
        if self.first_cast:
            self.log.debug(f"{self} found casted spell, boosting self")
            self.first_cast = False
            if self.triplet:
                hlt_boost = 4
            else:
                hlt_boost = 2
            self.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(self, 0, hlt_boost)
