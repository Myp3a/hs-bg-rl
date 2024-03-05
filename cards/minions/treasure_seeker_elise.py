from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .golden_monkey import GoldenMonkey

if TYPE_CHECKING:
    from models.army import Army


class TreasureSeekerElise(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 133
        self.classes = []
        self.level = 4
        self.base_attack_value = 5
        self.base_health_value = 5
        self.rolls_left = 5
        self.hooks["on_roll"].append(self.roll)
      
    def roll(self):
        self.rolls_left -= 1
        if self.rolls_left == 0:
            self.army.player.view.remove(random.choice(self.army.player.view))
            gm = GoldenMonkey(None)
            gm.triplet = True
            self.army.player.view.add(gm, len(self.army.player.view.cards))
            self.rolls_left = 5
