from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class BazaarDealer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 100
        self.classes = [MinionClass.Demon]
        self.level = 4
        self.base_attack_value = 2
        self.base_health_value = 4
        # TODO: tavern spells
