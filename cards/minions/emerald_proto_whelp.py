from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class EmeraldProtoWhelp(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 2
        self.classes = [MinionClass.Dragon]
        self.level = 1
        self.base_attack_value = 0
        self.base_health_value = 4
        self.hooks["on_turn_end"].append(self.increase_attack)

    def increase_attack(self) -> None:
        self.attack_perm_boost += 1
        if self.triplet:
            self.attack_perm_boost += 1