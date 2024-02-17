from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Cubling(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 8
        self.classes = [MinionClass.Undead]
        self.level = 1
        self.taunt = True
        self.base_attack_value = 0
        self.base_health_value = 1
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
