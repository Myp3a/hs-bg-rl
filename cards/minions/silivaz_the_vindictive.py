from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SilivazTheVindictive(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 203
        self.classes = [MinionClass.Naga]
        self.level = 6
        self.base_attack_value = 5
        self.base_health_value = 8
        # TODO: tavern spells
