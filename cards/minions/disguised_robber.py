from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class DisguisedRobber(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 105
        self.classes = []
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.destroy_undead)

    def destroy_undead(self) -> None:
        targets = [t for t in self.army.cards if MinionClass.Undead in t.classes]
        if len(targets) == 0:
            return
        target = random.choice(targets)
        self.army.cards.remove(target)
        self.army.player.tavern.sell(target)
        self.army.player.gold += 3
        if self.triplet:
            self.army.player.gold += 3
