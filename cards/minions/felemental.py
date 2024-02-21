from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Felemental(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 70
        self.classes = [MinionClass.Demon, MinionClass.Elemental]
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 1
        self.hooks["battlecry"].append(self.boost_tavern)

    def boost_tavern(self) -> None:
        self.army.player.tavern_attack_boost += 1
        self.army.player.tavern_health_boost += 1
