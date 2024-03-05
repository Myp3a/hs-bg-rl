from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class LandLubber(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 110
        self.classes = [MinionClass.Elemental, MinionClass.Pirate]
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 5
        # TODO: tavern spells