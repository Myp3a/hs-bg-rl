from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion

if TYPE_CHECKING:
    from models.army import Army


class GameEntity(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.base_attack_value = 0
        self.base_health_value = 1
