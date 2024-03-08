from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Baltharak(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 141
        self.classes = [MinionClass.Mech, MinionClass.Demon]
        self.level = 5
        self.base_attack_value = 10
        self.base_health_value = 1
        self.base_reborn = True
        self.magnetic = True
