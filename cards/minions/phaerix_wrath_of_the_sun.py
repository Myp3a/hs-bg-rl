from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class PhaerixWrathOfTheSun(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 84
        self.classes = []
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 1
        self.avenge_cntr = 4
        self.divine_shield = True
        self.hooks["on_sell"].append(self.remove_hook)
        self.hooks["on_turn_start"].append(self.reset_avenge)
        self.hooks["on_turn_end"].append(self.put_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_minion_death"].append(self.on_another_death)

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_death"].remove(self.on_another_death)

    def on_another_death(self, died, position) -> None:
        if self.health_value > 0:
            if not died is self:
                self.avenge_cntr -= 1
            if self.avenge_cntr == 0:
                self.give_shield()
                self.reset_avenge()

    def reset_avenge(self) -> None:
        self.avenge_cntr = 4

    def choose_and_give_shield(self) -> None:
        targets = [t for t in self.army.cards if not t.divine_shield]
        if len(targets) == 0:
            return
        target = random.choice(targets)
        target.divine_shield = True

    def give_shield(self):
        if self.triplet:
            self.choose_and_give_shield()
        self.choose_and_give_shield()
