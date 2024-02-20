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
        self.army.hooks["on_spell_cast"].append(self.boost_health)
        self.hooks["on_turn_start"].append(self.reset_first_cast)

    def reset_first_cast(self) -> None:
        self.first_cast = True

    def boost_health(self, casted) -> None:
        if self.first_cast:
            self.health_perm_boost += 2
            self.first_cast = False
            if self.triplet:
                self.health_perm_boost += 2