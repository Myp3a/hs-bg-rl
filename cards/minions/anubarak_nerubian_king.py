from __future__ import annotations
from typing import TYPE_CHECKING
from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class AnubarakNerubianKing(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 96
        self.classes = [MinionClass.Undead]
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 3
        self.hooks["deathrattle"].append(self.boost_undead_attack)

    def boost_undead_attack(self, position: int):
        if self.triplet:
            atk_boost = 2
        else:
            atk_boost = 1
        self.log.debug(f"{self} boosting {self.army.player} undead by {atk_boost} atk")
        self.army.player.undead_attack_boost += atk_boost
