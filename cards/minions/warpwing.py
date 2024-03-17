from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Warpwing(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 206
        self.classes = [MinionClass.Dragon]
        self.level = 6
        self.base_attack_value = 12
        self.base_health_value = 4
        self.immune_attack = True
