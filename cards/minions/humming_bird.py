from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class HummingBird(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 37
        self.classes = [MinionClass.Beast]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 4
