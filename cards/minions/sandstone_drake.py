from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SandstoneDrake(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 170
        self.classes = [MinionClass.Elemental, MinionClass.Dragon]
        self.level = 5
        self.base_attack_value = 0
        self.base_health_value = 9
        self.hooks["on_turn_end"].append(self.boost_attack)

    def boost_attack(self):
        for _ in range(len(self.army.player.cards_played_on_turn + 1)):
            if self.triplet:
                atk_boost = 2
            else:
                atk_boost = 1
            self.attack_perm_boost += atk_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(self, atk_boost, 0)
