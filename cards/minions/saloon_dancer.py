from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SaloonDancer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 126
        self.classes = []
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 5
        self.base_taunt = True
        # TODO: tavern spells
