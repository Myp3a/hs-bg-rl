from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class GraveGobbler(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 36
        self.classes = [MinionClass.Undead]
        self.level = 2
        self.base_attack_value = 4
        self.base_health_value = 3
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["on_turn_start"].append(self.destroy_left)

    def destroy_left(self) -> None:
        # TODO: find out triplet and rebirth mechanic
        pos = self.army.index(self)
        if pos > 0:
            to_the_left = self.army[pos-1]
            if MinionClass.Undead in to_the_left.classes:
                if to_the_left.rebirth:
                    to_the_left.rebirth = False
                else:
                    self.army.remove(to_the_left)
                self.attack_value += 5
                self.health_value += 5
