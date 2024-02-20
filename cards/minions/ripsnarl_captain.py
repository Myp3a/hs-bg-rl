from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RipsnarlCaptain(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 49
        self.classes = [MinionClass.Pirate]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 4
        self.army.hooks["on_attack"].append(self.boost_pirate_attack)

    def boost_pirate_attack(self, attacker: Minion, target) -> None:
        if MinionClass.Pirate in attacker.classes:
            attacker.attack_temp_boost += 3
