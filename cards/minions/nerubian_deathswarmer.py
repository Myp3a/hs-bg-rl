from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class NerubianDeathswarmer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 45
        self.classes = [MinionClass.Undead]
        self.level = 2
        self.base_attack_value = 1
        self.base_health_value = 4
        self.hooks["battlecry"].append(self.boost_undead_attack)

    def boost_undead_attack(self) -> None:
        self.army.player.undead_attack_boost += 1
