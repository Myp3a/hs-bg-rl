from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MonstrousMacaw(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 78
        self.classes = [MinionClass.Beast]
        self.level = 3
        self.base_attack_value = 5
        self.base_health_value = 3
        self.hooks["on_attack_mid"].append(self.trigger_deathrattle)

    def choose_and_trigger_deathrattle(self, position):
        targets = [t for t in self.army.cards if len(t.hooks["deathrattle"]) > 0]
        if not targets:
            self.log.debug(f"{self} found no targets")
            return
        target = random.choice(targets)
        self.log.debug(f"{self} triggering deathrattle for {target}")
        for hook in target.hooks["deathrattle"]:
            hook(self.army.index(target) + 1)

    def trigger_deathrattle(self, position):
        if self.triplet:
            self.choose_and_trigger_deathrattle(position)
        self.choose_and_trigger_deathrattle(position)
