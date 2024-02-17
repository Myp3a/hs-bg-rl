from __future__ import annotations
from typing import TYPE_CHECKING
from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class AnnoyOTron(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.classes = [MinionClass.Mech]
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 2
        self.health_value = self.base_health_value
        self.attack_value = self.base_attack_value
        self.divine_shield = True
        self.taunt = True
