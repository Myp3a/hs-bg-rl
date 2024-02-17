from __future__ import annotations
from typing import TYPE_CHECKING
from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RisenRider(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.classes = [MinionClass.Undead]
        self.level = 1
        self.base_attack_value = 2
        self.base_health_value = 1
        self.health_value = self.base_health_value
        self.attack_value = self.base_attack_value
        self.rebirth = True
        self.taunt = True
