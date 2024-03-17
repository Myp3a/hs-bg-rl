from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class NalaaTheRedeemer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 199
        self.classes = []
        self.level = 6
        self.base_attack_value = 5
        self.base_health_value = 7
        # TODO: tavern spells
