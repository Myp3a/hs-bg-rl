from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Murozond(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 165
        self.classes = [MinionClass.Dragon]
        self.level = 5
        self.base_attack_value = 5
        self.base_health_value = 5
        # TODO: get a card from last opponent's army