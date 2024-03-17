from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class WhirlingLassOMatic(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 207
        self.classes = [MinionClass.Mech]
        self.level = 6
        self.base_attack_value = 9
        self.base_health_value = 2
        self.base_windfury = True
        self.base_divine_shield = True
        # TODO: tavern spells
