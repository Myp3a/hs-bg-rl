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
        self.base_divine_shield = True
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_turn_start"].append(self.reset_avenge)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_death")
        self.army.hooks["on_minion_death"].append(self.on_another_death)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_death")
        self.army.hooks["on_minion_death"].remove(self.on_another_death)

    def on_another_death(self, died, position) -> None:
        if self.health_value > 0 and self in self.army.cards:
            if not died is self:
                self.avenge_cntr -= 1
            self.log.debug(f"{self} decreased avenge, new cntr {self.avenge_cntr}")
            if self.avenge_cntr == 0:
                self.give_shield()
                self.reset_avenge()

    def reset_avenge(self) -> None:
        self.avenge_cntr = 4

    def choose_and_give_shield(self) -> None:
        targets = [t for t in self.army.cards if not t.divine_shield]
        if not targets:
            self.log.debug(f"{self} found no targets")
            return
        target = random.choice(targets)
        self.log.debug(f"{self} giving shield to {target}")
        target.feature_overrides["shield"].append({"state": True, "one_turn": True})

    def give_shield(self):
        if self.triplet:
            self.choose_and_give_shield()
        self.choose_and_give_shield()
